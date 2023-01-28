## This is a documentation for Database module

The database is representing a form and answers of people to this form.
Also, there are users and some auxiliary tables.

### The main concept
There are leaders and projects as main objects, so there is a form for
leaders and a form for projects. Each form consists of Question Blocks.
Every Question Blocks consists of questions, but:
1. Questions might form a fixed table like this:
```
+---------+------------------+------------------+
|         | Morning activity | Evening activity |
+---------+------------------+------------------+
| Manager |                  |                  |
+---------+------------------+------------------+
| Worker  |                  |                  |
+---------+------------------+------------------+
```
2. Questions might form a Question table like this:
```
+---------------+------------------+------------------+
| Your project  | Your role in it  | Your part in it  |
+---------------+------------------+------------------+
|               |                  |                  |
+---------------+------------------+------------------+
|               |                  |                  |
+---------------+------------------+------------------+
...
```
3. In the example above question `Your project` is a relational question.
I.e. it describes a relation between a leader (respondent) and a project.
For relational projects there are extra settings, which are called
Relational Settings.
4. All the visualization and formatting settings are stored as 
Formatting Settings object.
5. There also could be multiple-choice questions or checkbox questions.
Answer to such questions can also be edited as 
Answer Options of one Answer Block. For example:
```
Choose your experience level:
- Beginner
- Experienced
- Expert
```
So there these 3 are Answer Options which form an Answer Block.
6. Long Text answers could be marked with tags. So there are Tag Types 
(similar to Answer Blocks). 
And tags, which are connected with some Tag Types.
7. Answers are stored using one-hot technique for different answer types.
different foreign keys and enum values are ment to be just integer 
values in the database. So basically there are only 3 types:
   1. Integer
   2. Timestamp
   3. Text
8. All points on map (cities, towns, districts, etc.) are stored in 
Toponyms table.
9. All users with their roles are stored in Users table
10. Editable Mixin is a mixin for most of ORM Classes - it saves 
info about creation and edit time of the table row. And uses the id 
as primary key
11. All the database history of changes is stored in Actions table

Now let's discuss each non-trivial table in the database:
### Answers
Each answer has such fields:
1. `table_row` - if this is an answer for a Question Table, 
what raw does it belong
2. `question_id` - id of question it answers
3. `leader_id` / `project_id` - which respondent provided this answer
4. `int_value` / `text_value` / `timestamp_value` - the answer stored 
as one-hot 

### Formatting Settings
1. `block_sorting` - questions are sorted in a block by this key
2. `table_column` / `table_row` - if the question is a part of a 
Question Table of a Fixed Table, what column and (optionally) row
it represents?
3. `block_id` - what block contains this question
4. `table_id` - what Question Table contains this question
5. `fixed_table_id` - what Fixed Table contains this question

### Question
1. `text` - obvious
2. `comment` - a hint that will be shown when user needs a hint
3. `question_type` - one of:
   1. Date
   2. User
   3. Long text
   4. Short text
   5. Multiple choice
   6. Checkbox
   7. Location
   8. Number
   9. Relation
4. `answer_block_id` - if the question is multiple choice or checkbox, 
what is the corresponding Answer Block
5. `tag_type_id` - if the question is long text, what type of tags is 
applicable
6. `show_on_main_page` - should the answer to this question be shown 
on the main page with these objects?
7. `formatting_settings` and `relation_settings` - links to the 
corresponding settings objects

### Relation Settings
1. `show_in_related` - does this relation need to be shown as a part
the related object form results?
2. `related_visualization_type` - if previous is True, then how to
show it:
   1. Full information
   2. Only name this object
   3. ... might be more options
3. `related_visualization_sorting` - key for sorting the answer between 
related answer blocks
4. `export_forward_relation` and `forward_relation_sheet_name` - 
does this relation need to be exported in Excel as one more sheet.
If yes, then how to call this sheet
5. `export_inverse_relation` and `inverse_relation_sheet_name` - 
the same, but with inverse relation (for example instead of 
leader-project we'll look at project-leader)

### Tags and Toponyms are stored as Trees

### Users
1. `login` provides uniqueness and login for a user
2. `name` - full name to describe user to others
3. `comment` - some info about who is this user (filled by admin)
4. `password_salt` is added to password before hashing
5. `password_hash` is a hash of password + salt
6. `role` describes permissions of this user:
   1. Unauthorized (if user tries to access something without 
logging in)
   2. Guest (can see something, can edit nothing)
   3. Intern (can see and edit something)
   4. Editor (can see everything, can change everything except for
form questions and other users' roles and permissions)
   5. Admin (can everything)
7. `jwt_refresh` - a JSON web refresh token stored in a DB

### Actions
1. `user_id` - who made the change
2. `ip` - from what IP address did he/she made the change
3. `table_id` and `column_id` - what column of what table had been changed
4. `row_id` - the id of a changed object
5. `timestamp` - when did the change took place
6. `value_int`, `value_datetime`, `value_text`, `value_bool` - one hot
stored new changed value of the cell.


`initialize_database.py` contains only one function which creates 
all the missing tables in the DB
