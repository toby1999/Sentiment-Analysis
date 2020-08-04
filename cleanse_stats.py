import pandas as pd
spreadsheet = pd.read_excel ('Data/coursecheck_data.xlsx') # Open spreadsheet

dataset = pd.DataFrame(spreadsheet,
                       columns= ['Training Company', 'Course Name',
                                 'Trainer name', 'Location', 'General Comments',
                                 'More comments 1', 'Overall Score (1-5)',
                                 'Review Date'])

total_comments = 0
blank_comments = 0
reviews_with_errors = 0
errors = 0

substring = 'Äô'

comments = {}

for row in spreadsheet.itertuples():
    total_comments += 1
    comment = str(row[11])
    if comment == 'nan':
        blank_comments += 1
        continue
    if substring in comment:
        reviews_with_errors += 1
    comments[comment] = comments.get(comment, 0) + 1
    errors += comment.count(substring)

duplicates = (total_comments-blank_comments) - len(comments)
usable_comments = total_comments - blank_comments - duplicates

print('Total comments: ', total_comments)
print('Blank comments: ', blank_comments)
print('Non-blank comments: ', total_comments-blank_comments)
print('Reviews containing encoding errors: ', reviews_with_errors)
print('Total number of encoding errors: ', errors)
print('Duplicate comments: ', duplicates)
print('Total useable comments: ', usable_comments)