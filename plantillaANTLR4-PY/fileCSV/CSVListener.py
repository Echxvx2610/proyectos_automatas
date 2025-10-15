# Generated from CSV.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CSVParser import CSVParser
else:
    from CSVParser import CSVParser

# This class defines a complete listener for a parse tree produced by CSVParser.
class CSVListener(ParseTreeListener):

    # Enter a parse tree produced by CSVParser#csvFile.
    def enterCsvFile(self, ctx:CSVParser.CsvFileContext):
        pass

    # Exit a parse tree produced by CSVParser#csvFile.
    def exitCsvFile(self, ctx:CSVParser.CsvFileContext):
        pass


    # Enter a parse tree produced by CSVParser#row.
    def enterRow(self, ctx:CSVParser.RowContext):
        pass

    # Exit a parse tree produced by CSVParser#row.
    def exitRow(self, ctx:CSVParser.RowContext):
        pass


    # Enter a parse tree produced by CSVParser#TextField.
    def enterTextField(self, ctx:CSVParser.TextFieldContext):
        pass

    # Exit a parse tree produced by CSVParser#TextField.
    def exitTextField(self, ctx:CSVParser.TextFieldContext):
        pass


    # Enter a parse tree produced by CSVParser#QuotedField.
    def enterQuotedField(self, ctx:CSVParser.QuotedFieldContext):
        pass

    # Exit a parse tree produced by CSVParser#QuotedField.
    def exitQuotedField(self, ctx:CSVParser.QuotedFieldContext):
        pass


    # Enter a parse tree produced by CSVParser#EmptyField.
    def enterEmptyField(self, ctx:CSVParser.EmptyFieldContext):
        pass

    # Exit a parse tree produced by CSVParser#EmptyField.
    def exitEmptyField(self, ctx:CSVParser.EmptyFieldContext):
        pass



del CSVParser