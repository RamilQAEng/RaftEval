import typer
from raft_eval.evaluation_runner.evaluator import Evaluator
from raft_eval.data_utils.loaders import load_dataset
from raft_eval.logging_utils.logger import save_results
from raft_eval.utils.llm_client import LLMClient
from raft_eval.utils.knowledge_base import KnowledgeBaseRetriever

app = typer.Typer()

@app.command()
def evaluate(
    input_path: str = typer.Option("DataBase.xlsx", help="Path to input file."),
    output_path: str = typer.Option("output.xlsx", help="Path to save output."),
    metrics: str = typer.Option("all", help="Comma-separated list of metrics to evaluate."),
):
    typer.echo(f"🚀 Starting batch evaluation on {input_path}...")
    
    # Load data
    questions, contexts, answers, gold_answers = load_dataset(input_path)

    
    # Initialize evaluator
    evaluator = Evaluator(metrics=metrics.split(",") if metrics != "all" else "all")
    
    # Run evaluation
    results = evaluator.evaluate_batch(questions, contexts, answers, gold_answers)
    
    # Save results
    save_results(results, output_path)
    
    typer.echo(f"✅ Evaluation completed! Results saved to {output_path}.")

@app.command()
def interactive(
    metrics: str = typer.Option("all", help="Comma-separated list of metrics or 'all'"),
    llm_model: str = typer.Option("deepseek/deepseek-chat-v3-0324", help="LLM model name"),
    knowledge_base_path: str = typer.Option("DataBase.xlsx", help="Path to knowledge base Excel file")
):
    typer.echo("🤖 Interactive RAG evaluation mode (Ctrl+C to exit)")

    llm = LLMClient(model_name=llm_model)
    retriever = KnowledgeBaseRetriever(knowledge_base_path)
    evaluator = Evaluator(metrics=metrics.split(",") if metrics != "all" else "all")

    PROMPT_TEMPLATE = (
        "Ты — помощник, который отвечает на вопросы ТОЛЬКО на основе приведённого ниже контекста.\n"
        "Если нужной информации в контексте НЕТ — ответь строго фразой: \"нет информации\".\n\n"
        "Контекст:\n{context}\n\n"
        "Вопрос:\n{question}\n\n"
        "Ответ:"
    )

    while True:
        try:
            question = typer.prompt("Question")
            context = retriever.get_relevant_context(question)
            if context is None:
                context = "нет информации"
            prompt = PROMPT_TEMPLATE.format(context=context, question=question)

            answer = llm.generate_answer(prompt)

            result = evaluator.evaluate_single(question, context, answer)

            typer.echo("\n--- Результаты ---")
            typer.echo(f"Question: {question}")
            typer.echo(f"Context: {context}")
            typer.echo(f"LLM Answer: {answer}")
            typer.echo("Metrics:")
            for metric_name, score in result.items():
                typer.echo(f"  {metric_name}: {score}")
            typer.echo("-----------------\n")

        except KeyboardInterrupt:
            typer.echo("\n👋 Exiting interactive RAG mode.")
            break

if __name__ == "__main__":
    app()
