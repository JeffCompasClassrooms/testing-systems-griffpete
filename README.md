# MyDB

```
Init:
  ✓ Store filename
  ✓ Do not overite existing file
  ✓ Make list for new db

LoadStrings:
  ✓ Load empty list
  ✓ Loads single string
  ✓ Loads multiple strings

SaveString:
  ✓ Appends string new
  ✓ Appends string to existing
  ✓ Appends empty string

SaveStrings:
  ✓ Saves empty array
  ✓ Saves multiple strings
  ✓ Overwrites existing data
```


# Squirrel Server
```
DELETE squirrels id:
  ✓ Returns 204
  ✓ Returns 404
  ✓ Removes squirrel from database
  ✓ Delete specified squirrel

GET squirrel:
  ✓ Returns 200
  ✓ Returns json
  ✓ Returns 404

GET squirrels:
  ✓ Returns 200
  ✓ Returns json
  ✓ Returns empty list
  ✓ Returns squirrels list
  ✓ Returns multiple squirrels
  ✓ Returns ordered by id

POST squirrels:
  ✓ Returns 201
  ✓ Creates squirrel
  ✓ Creates multiple squirrels
  ✓ Assigns unique ids

PUT squirrel:
  ✓ Returns 204
  ✓ Returns 404
  ✓ Updates name
  ✓ Updates size
  ✓ Preserves id
```
