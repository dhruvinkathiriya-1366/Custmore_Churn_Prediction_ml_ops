import pandas as pd

train_df = pd.read_csv('data/feature/train.csv')

print('ChurnCategory unique values:')
print(train_df['ChurnCategory'].value_counts(dropna=False))
print()

print('ChurnReason unique values:')
print(train_df['ChurnReason'].value_counts(dropna=False).head(20))
print()

# Check if there's correlation with ChurnLabel
print('ChurnLabel vs ChurnCategory:')
print(pd.crosstab(train_df['ChurnLabel'], train_df['ChurnCategory']))
print()

print('ChurnLabel vs ChurnReason (top 5):')
top_reasons = train_df['ChurnReason'].value_counts().head(5).index
for reason in top_reasons:
    reason_data = train_df[train_df['ChurnReason'] == reason]['ChurnLabel'].value_counts().to_dict()
    print(f'{reason}: {reason_data}')
