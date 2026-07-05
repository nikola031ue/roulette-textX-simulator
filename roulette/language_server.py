from os.path import join, dirname
from textx import metamodel_from_file
from textx.exceptions import TextXSyntaxError, TextXSemanticError
from pygls.lsp.server import LanguageServer
from lsprotocol.types import (
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_COMPLETION,
    DidOpenTextDocumentParams,
    DidChangeTextDocumentParams,
    CompletionParams,
    CompletionList,
    CompletionItem,
    CompletionItemKind,
    Diagnostic,
    DiagnosticSeverity,
    Position,
    PublishDiagnosticsParams,
    Range,
    TextDocumentSyncKind,
)

GRAMMAR_PATH = join(dirname(__file__), "grammar.tx")

KEYWORDS = [
    ("bankroll",        CompletionItemKind.Keyword),
    ("round",           CompletionItemKind.Keyword),
    ("strategy",        CompletionItemKind.Keyword),
    ("bet",             CompletionItemKind.Keyword),
    ("spin",            CompletionItemKind.Keyword),
    ("clear_bets",      CompletionItemKind.Keyword),
    ("cash_out",        CompletionItemKind.Keyword),
    ("double_bet",      CompletionItemKind.Keyword),
    ("reset_bet",       CompletionItemKind.Keyword),
    ("stop_on_win",     CompletionItemKind.Keyword),
    ("stop_on_loss",    CompletionItemKind.Keyword),
    ("repeat",          CompletionItemKind.Keyword),
    ("while",           CompletionItemKind.Keyword),
    ("if",              CompletionItemKind.Keyword),
    ("if_win",          CompletionItemKind.Keyword),
    ("if_lose",         CompletionItemKind.Keyword),
    ("else",            CompletionItemKind.Keyword),
    ("break",           CompletionItemKind.Keyword),
    ("continue",        CompletionItemKind.Keyword),
    ("skip_round",      CompletionItemKind.Keyword),
    ("show_stats",      CompletionItemKind.Keyword),
    ("show_history",    CompletionItemKind.Keyword),
    ("show_balance",    CompletionItemKind.Keyword),
    ("number",          CompletionItemKind.EnumMember),
    ("red",             CompletionItemKind.EnumMember),
    ("black",           CompletionItemKind.EnumMember),
    ("even",            CompletionItemKind.EnumMember),
    ("odd",             CompletionItemKind.EnumMember),
    ("low",             CompletionItemKind.EnumMember),
    ("high",            CompletionItemKind.EnumMember),
    ("dozen",           CompletionItemKind.EnumMember),
    ("column",          CompletionItemKind.EnumMember),
    ("split",           CompletionItemKind.EnumMember),
    ("street",          CompletionItemKind.EnumMember),
    ("corner",          CompletionItemKind.EnumMember),
    ("sixline",         CompletionItemKind.EnumMember),
    ("basket",          CompletionItemKind.EnumMember),
    ("balance",         CompletionItemKind.Variable),
    ("consecutive_wins",   CompletionItemKind.Variable),
    ("consecutive_losses", CompletionItemKind.Variable),
    ("round_profit",    CompletionItemKind.Variable),
    ("and",             CompletionItemKind.Operator),
    ("or",              CompletionItemKind.Operator),
]

server = LanguageServer("roul-language-server", "v0.1", text_document_sync_kind=TextDocumentSyncKind.Full)


def _validate(ls: LanguageServer, uri: str, source: str):
    diagnostics = []
    try:
        mm = metamodel_from_file(GRAMMAR_PATH)
        mm.model_from_str(source)
    except (TextXSyntaxError, TextXSemanticError) as e:
        line = (e.line or 1) - 1
        col = (e.col or 1) - 1
        diagnostics.append(Diagnostic(
            range=Range(
                start=Position(line=line, character=col),
                end=Position(line=line, character=col + 10),
            ),
            message=e.message if hasattr(e, 'message') else str(e),
            severity=DiagnosticSeverity.Error,
            source="roul",
        ))
    except Exception as e:
        diagnostics.append(Diagnostic(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=1),
            ),
            message=str(e),
            severity=DiagnosticSeverity.Error,
            source="roul",
        ))
    ls.text_document_publish_diagnostics(
        PublishDiagnosticsParams(uri=uri, diagnostics=diagnostics)
    )


@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: LanguageServer, params: DidOpenTextDocumentParams):
    _validate(ls, params.text_document.uri, params.text_document.text)


@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: LanguageServer, params: DidChangeTextDocumentParams):
    doc = ls.workspace.get_text_document(params.text_document.uri)
    _validate(ls, params.text_document.uri, doc.source)


@server.feature(TEXT_DOCUMENT_COMPLETION)
def completion(_ls: LanguageServer, _params: CompletionParams):
    items = [
        CompletionItem(label=label, kind=kind)
        for label, kind in KEYWORDS
    ]
    return CompletionList(is_incomplete=False, items=items)


if __name__ == "__main__":
    server.start_io()
