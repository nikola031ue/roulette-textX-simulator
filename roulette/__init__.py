from os.path import dirname, join

from textx import metamodel_from_file
from textx.export import model_export
from textx.registration import generator, language

GRAMMAR_PATH = join(dirname(__file__), "grammar.tx")


def metamodel(**kwargs):
    return metamodel_from_file(GRAMMAR_PATH, **kwargs)


@language("roul", pattern="*.rul")
def roul_language():
    """Rulet DSL za simulaciju strategija igranja ruleta."""
    return metamodel()


@generator("roul", "dot")
def roul_dot_generator(metamodel, model, output_path, overwrite, debug=False, **custom_args):
    """Generise DOT vizualizaciju odigrane .rul strategije."""
    model_export(model, output_path or "model.dot")
