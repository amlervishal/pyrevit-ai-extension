"""
Revit API - Transaction Management Reference
Essential methods for managing transactions in Revit modifications.
"""

class TransactionAPI:
    """
    Transaction Class - Required for all document modifications
    Namespace: Autodesk.Revit.DB
    
    Transactions guard any changes made to a Revit model. All modifications
    to the model must occur within a transaction.
    """
    
    # TRANSACTION BASICS
    TRANSACTION_BASICS = {
        'Constructor': 'Transaction(Document doc, string name)',
        'Start()': 'TransactionStatus - Starts the transaction',
        'Commit()': 'TransactionStatus - Commits changes to the model',
        'RollBack()': 'TransactionStatus - Discards changes and rolls back',
        'GetStatus()': 'TransactionStatus - Gets current transaction status',
        'GetName()': 'string - Gets transaction name',
        'HasStarted()': 'bool - Indicates if transaction has started',
        'HasEnded()': 'bool - Indicates if transaction has ended'
    }
    
    # TRANSACTION STATUS ENUM
    TRANSACTION_STATUS = {
        'Uninitialized': 'Transaction not yet initialized',
        'Started': 'Transaction has been started',
        'Committed': 'Transaction has been committed',
        'RolledBack': 'Transaction has been rolled back',
        'Pending': 'Transaction is pending (in progress)',
        'Error': 'Transaction encountered an error'
    }

# BASIC USAGE PATTERNS
BASIC_PATTERNS = """
# Simple Transaction Pattern
using (Transaction trans = new Transaction(doc, "Operation Name"))
{
    trans.Start();
    
    // Perform modifications here
    Wall wall = Wall.Create(doc, line, wallTypeId, levelId, 10, 0, false, false);
    
    trans.Commit();
}

# Transaction with Error Handling
Transaction trans = new Transaction(doc, "Operation Name");
try
{
    trans.Start();
    
    // Perform modifications
    CreateElements(doc);
    
    trans.Commit();
}
catch (Exception ex)
{
    if (trans.HasStarted() && !trans.HasEnded())
    {
        trans.RollBack();
    }
    TaskDialog.Show("Error", ex.Message);
}
"""

# QUICK REFERENCE
QUICK_REFERENCE = {
    "Basic Transaction": "using (Transaction trans = new Transaction(doc, \"Name\")) { trans.Start(); ... trans.Commit(); }",
    "Check Transaction Status": "trans.GetStatus() == TransactionStatus.Started",
    "Rollback Transaction": "trans.RollBack()",
    "Transaction Name": "trans.GetName()",
    "Has Started": "trans.HasStarted()",
    "Has Ended": "trans.HasEnded()"
}
