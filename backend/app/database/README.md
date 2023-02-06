# This is a documentation for Database module

The database represents a form and answers of people to this form.
Also, there are users and some auxiliary tables.

## The main concept
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
Tags form a tree structure
7. Answers are stored using one-hot technique for different answer types.
different foreign keys and enum values are ment to be just integer 
values in the database. So basically there are only 4 types:
   - Integer
   - Timestamp
   - Text
   - Boolean
8. All points on the map (cities, towns, districts, etc.) are stored in 
Toponyms table.
9. All users with their roles are stored in Users table
10. Editable Mixin is a mixin for most of ORM Classes - it saves 
info about creation and edit time of the table row. And uses the id 
as primary key
11. All the database history of changes is stored in Actions table
12. Most of all ORM classes provide function `to_json()` that returns a
dictionary (a.k.a. `JSON`, a.k.a. `Dict[str, Any]`)
13. The idea is to use all the column values as private fields and provide
properties to get and, maybe, set the values.
14. If an object is [Editable](#Editable), the setters of editable properties
should be decorated with `Editable.on_edit`
15. No one can actually delete
anything from the database, so when you delete something, it just gets
marked as [`deleted`](#Editable), 
but you still can find it in the database.
By default, all the searches and queries filter only not deleted items,
but if you change a special `app_context` variable in a request,
the deleted objects will also be shown. 
(For more info check out [FlaskApp](../flask_app.py))
16. If the field should have translations to different languages,
the corresponding property in an ORM class returns and receives a
JSON object. And stores in a database field just like dumped json string.
```
{
   "ru": "В чем сила?",
   "en": "What is power?",
   "in": "apa itu kekuatan?"
}
```

Now let's discuss each table and its functions

## Action
A table to store the history of changes in the database.
Every `Action` row represents change of one column in one
row in one table. It stores only changes of tables, who are also derived
from [Editable](#Editable).

Each action stores such values:
- `user_id` (who made the change)
- `table_id` (where the change was made)
- `column_id`
- `row_id` (for `Users` table it's `users.id`, 
for `Questions` table it's `questions.id`, etc...)
- `ip` (the ip of the client who sent the request of the change)
- `timestamp` (when the change was made)
- `value` (it's actually a property that contains 4 columns for 4
types of value, but you can set and get it just as usual `value: Any`)

Action can be created using such arguments:
`Action(table_id, column_id, row_id, value)`
All the information about current user is received from `flask_jwt_extended`
Action objects are being created automatically when you call a setter of
a property, decorated with [`Editable.on_edit`](#Editable)

Actions provide a filter function:
`Actions.filter(user_id, timestamp_range, table_id, column_id, row_id, value)`

Every parameter is optional, you can pass None or just don't pass it.
- `user_id: int` filter by user who made the change
- `timestamp_range: TimestampRange` a [TimestampRange](#Enums)
object - the timestamp of change should be in these boundaries
- `table_id: int` filter by `table_id`
- `column_id: int` -//-
- `row_id: int` -//-
- `value: datetime | int | str | boolean` filter by value. 
If value is `str`, there will be a substring search. 
Otherwise, the exact match filter

Basically `Actions` is more like auxiliary table

## Answer
The table stores answers to all questions of all types.
Each answer has such fields:
- `table_row` - if this is an answer for a Question Table, 
what raw does it belong
- `question_id` - id of question it answers
- `form_id` - which respondent provided this answer 
(either `leaders.id` or `projects.id`)
- `value` - property with the answer stored as one-hot

Answer has only `value` column editable. Other columns are set on creation
and stay unchanged.

Functions with Answer:

`__init__(question_id, form_id, value, table_row, row_question_id)`
- `question_id: int` - the id of the question is asked
- `value: int | datetime | str | boolean` - the value of the answer
  (foreign keys are ment to be `int`)
- `table_row: int` - if it's a question table, there might be many answers
  to this question, so you should provide a row index
- `row_question_id: int` - if it's a fixed table question, the answer is
determined by 2 question: a row question and a column question, so the
column question id is stored in `question_id` field, the row question 
id is stored here

`count_with_condition(ids, condition)`\
Returns the number of respondents
with id from the given set that satisfy the condition
- `ids: List[int]` the list of `leader.id` or `project.id` to search in
- `condition` - sqlalchemy condition like `Answer.value_int > 0` or
`Answer.value_str.like("%aboba%")`

`get_extremum(question_id, question_type, extremum)`\
Returns the extremum (minimum if `extremum: ExtremumType` is `MINIMUM`,
maximum otherwise) 
value from all answers to the question with
`question_id: int` of type `question_type: QuestionType` 
(the type should be either `DATETIME` or `NUMBER`)

`count_forms_answers(form_id: int, question_id: int)`\
Returns the number of leader's or project's answers to the question with
id `question_id` (used with question table questions)


`count_distinct_answers(query, question_id)`\
Returns the number of different answers to the question with id 
`question_id: int` in the given `query: Query`

`filter(question_id, row_question_id, form_id, exact_value, min_value, max_value, substring)`\
Returns a list of `Answer` objects, filtered by conditions 
(all the arguments are optional):
- `question_id: int`
- `form_id: int` the id of the respondent
- `exact_value: int | str | datetime | boolean` filter only exact match
- `min_value, max_value: int | datetime` filter only answers from this range
  (if one of these args is not passed, it will be replaced with maximum boundary)
- `substring: str` filter answers with value containing this string as substring

`get_distinct_filtered(question_id, exact_value, min_value, max_value, substring, row_question_id)`\
Similar to `filter`, but returns a list of distinct `form_id` values
(who gave answers matching such conditions?)

`_filter_query(question_id, row_question_id, form_id, exact_value, min_value, max_value, substring)`\
A private function for filter function. Returns a sqlalchemy query object
filtered by rules above

`query_for_question_ids(ids)`\
Returns the query object filtered 
only answers for questions with id value from this set
- `ids: Set[int]`

`query_question_grouped_by_forms(question_id)`\
Returns the query
object with answers to the question with `question_id: int`
grouped by `form_id`. (An auxiliary function to calculate statistics)

## AnswerBlock
A block with answer options. It's an editable object.
It stores only `name` - a translated property.

Functions with AnswerBlock:

`get_by_id(id)`\
Searches in the database for a row with given `id: int`
returns the found object or `None`

`get_all_blocks()`\
Returns the list of JSONs (each JSON is an AnswerBlock)

`to_json()` works non-trivial 
(it also includes list of options to the return value)

## AnswerOption
An option for checkbox question or a multiple-choice question
Properties:
`name` and `short_name` - all translated strings,
`answer_block_id: int`

Functions:

`get_all_from_block(block_id: int)`\
Returns a list of AnswerOption objects from a given block

## Editable
A base class (not a table) for editable objects 
(those objects, whose changes should be stored in the 
[Actions](#Action) table)
Fields:
- `id: int` (provides and ID for every editable object)
- `create_timestamp: datetime` (when the object was firstly created)
- `deleted: boolean` (is the item deleted?)

An `_edit(column_id, value, table_id)` is an auxiliary function
that says that self item at `table_id: int` with `column_id: str`
has changed value to `value: datetime | int | Enum | str | boolean`

You should use `Editable.on_edit` decorator for the property setter in
the derived class. If the written value is different from the argument,
the decorator should return the result value 
(for example, when you change the password, the setter receives 
the password and writes the hash, so it should return the hash)
Otherwise (if no return) the argument will be stored as a new value
The name of the setter function should be the same as 
the name of the property

## EditableValueHolder
The mix of [ValueHolder](#ValueHolder) and [Editable](#Editable)
Provides the correct changelog and filtering for a value stored
as one-hot.

`value` is a property that hides 4 table columns with one-hot storage
`filter_by_value(table, exact_value, min_value, max_value, substr)`\
Returns a sqlalchemy query that filters by value:
- `table: Type[FlaskApp()db.Model]` the ORM class for table to search in
- all other arguments are the same as in [Answer.filter()](#Answer)

Other functions are obvious auxiliary functions for 
the `filter_by_value` function

## FixedTable
An Editable object. It has property `block_sorting: int` - all the
items in a block are sorted using their `block_sorting` as a key

`get_by_ids(ids: Set[int])`\
Returns list of FixedTable objects with ids from a given set

`get_questions(with_answers, form_id)`\
Both arguments are optional. If none of them is set, returns just a json
like:
```
{
   "columns": List of questions' JSONs,
   "rows": List of questions' JSONs
}
```
Otherwise (if `with_answers` is True), the `form_id` should also
be passed, so the result is form filled with answers of a given respondent:
```
{
   "columns": List of questions' JSONs,
   "rows": List of questions' JSONs,
   "answers": [
      [some, answers, of, first, row],
      [some, answers, of, second, row],
      ...
   ]
}
```

`_get_only_questions` and `_get_questions_with_answers(form_id: int)`
are auxiliary functions that prepare the corresponding JSONs

## Form
This is a class to store leaders and projects.
It provides functions to work with them.

Properties:
- `state` FormState enum object 
(what is the state of a form? planned/started/finished)
- `name` a unique string name
- `form_type` is it a leader or a project


Functions:

`filter(question_id, exact_value, min_value, max_value, substring, row_question_id)`\
Returns the set of form ids where the `name_condition` 
(a sqlalchemy condition like `Project.name.like("%oices of%")`) 
is satisfied with filters the same as in [Answer](#Answer).
And filter by `row_question_id: int` 
(if the question is in a fixed table)

`prepare_statistics(question_id, min_value, max_value, step)`\
Returns the statistics for `table: Table class` for `question_id: int`.
If the answer value is `int` or `datetime` you should provide
`min_value: int | datetime`, `max_value: int | datetime` and `step: int`
If `min_value` or `max_value` is not provided, it will be replaced with 
minimum / maximum value in the database. 
If there are no records in the database and min/max value is not provided,
a `LogicException` will be thrown. If step is not provided, a `LogicException`
will be thrown. If the answer type is datetime, `step` means step in days.
The result is statistics (how many forms have such answers)
(Suppose this is a statistics for a question with options `a`, `b` and `c`)
```
{
   // There are different states of form
   "PLANNED": {
      "a": 179,
      "b": 57,
      "c": 2
   },
   "STARTED": {
      "a": 11,
      "b": 73,
      "c": 111
   },
   "FINISHED": {
      "a": 0,
      "b": 0,
      "c": 1
   }
}
```
And if the result type is `int` or `datetime`
(suppose, the question is date of birth and step is 10 years):
```
{
   "PLANNED": {
      "1950.01.01 - 1960.01.01": 2,
      "1960.01.01 - 1970.01.01": 3,
      "1970.01.01 - 1980.01.01": 5,
      "1980.01.01 - 1990.01.01": 8,
      "1990.01.01 - 2000.01.01": 13,
      "2000.01.01 - 2010.01.01": 21,
   },
   ...
}
```

`get_by_ids(ids: Set[int])` Returns all the forms with 
id from the given set

`_filter_by_answers_count(question_id, min_answers_count, max_answers_count)`\
Returns set of forms' ids where the number of answers to question with id
`question_id: int` is in range from `min_answers_count: int` inclusively
to `max_answers_count: int` exclusively.

Other functions are just auxiliary for the statistics preparations

## Formatting Settings
An object related one-to-one with questions. Describes the question
formatting.
1. `block_sorting` - questions are sorted in a block by this key
2. `table_column` / `table_row` - if the question is a part of a 
Question Table of a Fixed Table, what column and (optionally) row
it represents?
3. `block_id` - what block contains this question
4. `table_id` - what Question Table contains this question
5. `fixed_table_id` - what Fixed Table contains this question

Functions:

`get_by_id(id: int)` Returns object with such `id` from DB or `None`

`query_from_block(block_id: int)`\
Returns a sqlalchemy query object filtered only from a given block

`get_from_question_table(question_table_id: int)`\
Returns list of FormattingSettings objects from given question table

`get_from_fixed_table(fixed_table_id: int)` - the same as previous
but with fixed table

`filter_only_[free/table/fixed_table]_questions(query: Query)`\
Returns list of FormattingSettings objects from this query, but
only asked kind of items

## PrivacySettings
An object, associated by 1 to 1 connection with a question,
that describes privacy of the answers to this question.
`AccessType` is an Enum of types of access 
(can nothing / can see / can edit)

Properties:
- `editor_access`
- `intern_access`
- `guest_access`

All the properties are `AccessType`

PrivacySettings provide `get_by_id(id: int)` function

## Question
1. `text` - translated question text
2. `comment` - a translated hint that will be shown when user 
needs a hint
3. `question_type` - [QuestionType](question_type.py)
4. `answer_block_id` - if the question is multiple choice or checkbox, 
what is the corresponding Answer Block
5. `tag_type_id` - if the question is long text, what type of tags is 
applicable
6. `show_on_main_page` - should the answer to this question be shown 
on the main page with these objects?
7. `formatting_settings`, `relation_settings` and `privacy_settings`
are links to the corresponding settings objects

Functions:

`__init__(texts, question_type, comment, answer_block_id, tag_type_id)`\
Does not require settings objects. It is supposed that they will be
added later during the initialization

`prepare_my_table(inverse_relation: bool)`\
Prepares a table for export to Excel with this question.
If this table should not be exported, the function returns `None`.
If it's a question table question, it collects all the information
about other questions and answers and creates a table.
Otherwise, it'll be just a column. The format anyway is this:
```
{
    "questions": [
        {
            "id": 179,
            "text": {
                "en": "Why do you work?",
                ...
            },
            ...
        },
        {
            "id": 123,
            "text": {
                "en": "How many children do you have?",
                ...
            },
            ...
        },
        ...
    ],
    "answers": [
        {
            "179": "Because I love my work",
            "123": 3,
            ...
        },
        {
            "179": "Because I need money",
            "123": 4,
            ...
        },
        ...
    ]
}
```

`filter_by_answer_block(block_id: int)`\
Returns a sqlalchemy query object filtered only questions with a given
answer block

`get_by_id(id: int)` and `get_by_ids(ids: List[int])`\
Returns one or list of Question objects with id from a given list /
equals to given

`get_all_with_formattings(formattings: List[FormattingSettings])`\
Returns a list of question objects who are associated with formattings
from the list

`get_by_text(text: str)`\
Returns a list of questions which have the given text as a substring

`to_json(with_answers: bool, form_id: int)`\
Returns a json, but if `with_answers` is True,
you should also provide `form_id` - the id of the form to get answers from.
If `with_answers`, in result JSON also will be a field `answers` -
list of answer jsons for every answer from a given form to this question.

## QuestionBlock
A block with questions. It can contain free questions, 
fixed tables and question tables.

Fields:
- `form` a `FormType` enum object. Is this block in a leader form or
in a project form
- `name` a translated text that shows at the top of the block
- `sorting` a key used when blocks are sorted on the page

Functions:

`get_form(form: FormType)`\
Returns a list of question blocks in the correct order 
(as they should be shown on the page).

`get_questions(with_answers, form_id)`\
Returns a list of JSONs with questions and tables.
Items are sorted as they should appear on the page.
The result has such format:
```
[
  {
    "type": "question",
    "value": {
      "text": "this is just a question",
      ...
    }
  },
  {
    "type": "table_question",
    "value": {
      "columns": [
        {
          "text": "this is a question as a column in a table",
          ...
        },
        {...}
      ]
    }
  },
  {
    "type": "fixed_table_question",
    "value": {
      "columns": [
        {
          "text": "this is a question as a column in a fixed table",
          ...
        },
        {...}
      ],
      "rows": [
        {
          "text": "this is a question as a row in a fixed table",
          ...
        },
        {...}
      ]
    }
  },
  {...}
]
```
If `with_answers` is True, the questions will be exported with answers
from form with id `form_id`.

`_get_free_questions`, `_get_table_questions` and `_get_fixed_table_questions`
are auxiliary functions for function `get_questions`

`to_json()` has field `questions` containing the result of
`get_questions`

## QuestionTable
Has only property `block_sorting` describing the key for sorting with
other objects inside one block.

Functions:

`get_by_ids(ids: Set[int])`\
Returns a list of QuestionTable objects with ids from a given set

`get_questions(with_answers, form_id)`\
Returns a list of JSONs for questions with or without answers.
Questions are sorted as should be sorted table columns.

## RelationSettings
A 1 to 1 associated with `Question` object that describes
settings of a relational question.

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

`get_by_id(id: int)` Returns an object with a given ID or `None`.

`get_foreign_to_show_query(form: FormType)`\
Returns a sqlalchemy query object containing only
`RelationSettings.id` and `RelationSettings.related_visualization_type`
 filtered only items which should be shown on the page of the `form`
as the foreign questions (so they're not this respondent questions,
but if respondent answers with link to this object, we show it on the
page of this object).

## Tag
Tags are stored as a set of trees. Each element either has no parent
(i.e. it is a root node) or has one parent.
Properties:
- `text` translated name of the tag
- `type_id` the id of the `TagType` object which contains this tag
- `parent_id` the id of the parent node (`None` if this is root)
- `children` (not a field actually) returns a list of all
items who have this node as parent

Functions:

`build_tree()`\
Returns a subtree of this node stored as this:
it is a usual `to_json()` call, but it also contains field `children`
with list of their same-formatted jsons (recursively).
This function makes O(n) database queries. It could be done with O(1)
database queries, but it should use more of thinking, so I decided 
firstly to implement a simple variant.

`get_all_of_type(type_id: int)`\
Returns a list of `Tag` items from a given TagType, not structured.

`get_roots_of_type(type_id: int)`\
Returns a list of items who are roots in this type.
If call `build_tree()` on every of them, you will get all the trees for
the given type.

`get_ancestors()`\
Returns a list of tags (path from this tag to it's root)

## TagToAnswer
A relation between tags and answers.
It's not an Editable object - it's just a usual table.
Properties:
- `id` (primary key)
- `tag_id`
- `answer_id`

Functions:

`count_tag_usage(tag_id: int)`\
Returns the number of usages of a given tag

`get_answers_tags_ids(answer_id: int)`\
Returns a list of tag ids associated with a given answer

`add_tag/remove_tag(tag_id: int, answer_id: int)`\
Adds or removes a given tag to or from a given answer

## TagType
Tag type contains some tag trees.
But as an object it stores only a `text` - translated name of the tag type.

Functions:

`get_tags()` Returns a list of tags of this type

`get_forest()` Returns a forest (JSON list of trees) with tags of this type

`to_json()` contains a field `tags` with the forest

`get_all_names()` Returns a list of all tag types

`get_all_blocks()` Returns a list of all JSONs (with tags) of TagTypes

##  Toponym
Any Toponym object represents some area on the map. Toponyms form a tree
by their nesting.
Toponyms cannot be edited, so they can be only uploaded and changed by 
the developers.

Each toponym has:
- `id`
- `name` (just string without translation)
- `parent_id`
So the structure is similar to [Tag](#Tag)

Functions:

`get_all()` Returns the list of all Toponyms

`get_by_name(name: str)` Searches for an exact match of the name
and returns the item or `None`

`get_ancestors()` Similar to the same function if [Tag](#Tag)

`search_by_name(name_substring: str)` Returns a list of all
toponyms with name containing given substring

## User
User properties:
1. `login` provides uniqueness and login for a user
2. `name` - full name to describe user to others
3. `comment` - some info about who is this user (filled by admin)
4. `password_salt` is added to password before hashing
5. `password_hash` is a hash of password + salt
6. `role` describes permissions of this user:
   1. Guest (can see something, can edit nothing)
   2. Intern (can see and edit something)
   3. Editor (can see everything, can change everything except for
form questions and other users' roles and permissions)
   4. Admin (can everything)
7. `jwt_refresh` - a JSON web refresh token stored in a DB

I do not provide a documentation for a User class, because Lev will 
change it soon...

## ValueHolder
An auxiliary class (not a Table) that stores a value as one-hot.
It has 4 fields:
- `value_int`
- `value_str`
- `value_datetime`
- `value_bool`

And property `value` that wraps those 4 fields

## Enums and auxiliary classes
There are also a lot of important enums:
- [ExtremumType](answer.py) MINIMUM or MAXIMUM
- [FormState](form.py) what is the state (status) of form? 
planned/started/finished
- [FormType](form_type.py) LEADER or PROJECT
- [AccessType](privacy_settings.py) The level of access 
of some role to some question
- [QuestionType](question_type.py) The type of the answer to the question
- [RelationType](relation_type.py) LeaderToLeader, LeaderToProject, etc...
- [TimestampRange](timestamp_range.py) A range from...to of datetime
- [Role](user.py) A role of a user (ADMIN, GUEST, etc...)
- [VisualizationType](visualization_type.py) How to show
the rows of the question table in the other (linked) object?