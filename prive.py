# prive.py

import typer
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

app = typer.Typer()

@app.command()
def scan(file_path: str):
    """
    Scan a file for PII using Microsoft Presidio.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        typer.echo(f"Error reading file: {e}")
        raise typer.Exit(code=1)

    # Set up the NLP engine for Presidio
    provider = NlpEngineProvider(nlp_configuration={
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": "en_core_web_lg"}],
    })
    nlp_engine = provider.create_engine()

    # Initialize the AnalyzerEngine with the NLP engine
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["en"])

    # Analyze the text
    results = analyzer.analyze(text=text, language="en")

    if results:
        typer.echo("PII Detected:")
        for result in results:
            pii_text = text[result.start : result.end]
            typer.echo(
                f"- {result.entity_type} at position {result.start}-{result.end}: {pii_text}"
            )
    else:
        typer.echo("No PII detected.")

if __name__ == "__main__":
    app()
