"""
Revit API - Advanced Transaction Management
Transaction Groups and Sub-Transactions
"""

class TransactionGroupAPI:
    """
    TransactionGroup - Groups multiple transactions together
    Useful for complex operations that require multiple transaction steps
    """
    
    TRANSACTION_GROUP = {
        'Constructor': 'TransactionGroup(Document doc, string name)',
        'Start()': 'TransactionStatus - Starts the transaction group',
        'Assimilate()': 'TransactionStatus - Combines all transactions in group',
        'RollBack()': 'TransactionStatus - Rolls back entire group',
        'GetStatus()': 'TransactionStatus - Gets group status',
        'IsActive()': 'bool - Indicates if group is active'
    }

class SubTransactionAPI:
    """
    SubTransaction - For temporary modifications within a transaction
    Useful for temporary changes that need to be rolled back
    """
    
    SUB_TRANSACTION = {
        'Constructor': 'SubTransaction(Document doc)',
        'Start()': 'void - Starts the sub-transaction',
        'Commit()': 'void - Commits the sub-transaction',
        'RollBack()': 'void - Rolls back the sub-transaction',
        'HasStarted()': 'bool - Indicates if sub-transaction has started'
    }

# ADVANCED PATTERNS
ADVANCED_PATTERNS = """
# Transaction Group Pattern
using (TransactionGroup transGroup = new TransactionGroup(doc, "Multiple Operations"))
{
    transGroup.Start();
    
    using (Transaction trans1 = new Transaction(doc, "Operation 1"))
    {
        trans1.Start();
        // First set of modifications
        trans1.Commit();
    }
    
    using (Transaction trans2 = new Transaction(doc, "Operation 2"))
    {
        trans2.Start();
        // Second set of modifications
        trans2.Commit();
    }
    
    transGroup.Assimilate(); // Combine all transactions
}

# Sub-Transaction for Temporary Changes
using (Transaction trans = new Transaction(doc, "Main Operation"))
{
    trans.Start();
    
    // Main modifications
    PerformMainOperations();
    
    // Temporary changes for calculation
    using (SubTransaction subTrans = new SubTransaction(doc))
    {
        subTrans.Start();
        
        // Temporary modifications
        MakeTemporaryChanges();
        
        // Perform calculations
        CalculateResults();
        
        // Roll back temporary changes
        subTrans.RollBack();
    }
    
    // Apply final modifications
    ApplyFinalChanges();
    
    trans.Commit();
}
"""
