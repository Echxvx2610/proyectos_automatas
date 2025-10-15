# Generated from CSV.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CSVParser import CSVParser
else:
    from CSVParser import CSVParser

# This class defines a complete generic visitor for a parse tree produced by CSVParser.

class CSVVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CSVParser#csvFile.
    def visitCsvFile(self, ctx:CSVParser.CsvFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CSVParser#row.
    def visitRow(self, ctx:CSVParser.RowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CSVParser#TextField.
    def visitTextField(self, ctx:CSVParser.TextFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CSVParser#QuotedField.
    def visitQuotedField(self, ctx:CSVParser.QuotedFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CSVParser#EmptyField.
    def visitEmptyField(self, ctx:CSVParser.EmptyFieldContext):
        return self.visitChildren(ctx)



del CSVParser