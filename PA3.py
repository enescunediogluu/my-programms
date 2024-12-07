import sys

def print_table(headers,rows):
    column_widths = []
    for header in headers:
        column_widths.append(len(header))

    for row in rows:
        for i in range(len(row)):
            column_widths[i] = max(column_widths[i], len(str(row[i])))

    top_border = "+"
    for i in range(len(column_widths)):
        top_border += "-" * (column_widths[i] + 2) + "+"
    print(top_border)

    header_row = "|"
    for i in range(len(headers)):
        header_row += f" {headers[i]: <{column_widths[i]}} |"
    print(header_row)

    print(top_border)

    for row in rows:
        data_row = "|"
        for i in range(len(row)):
            data_row += f" {str(row[i]): <{column_widths[i]}} |"
        print(data_row)

    print(top_border)

def create(line,tables):

    table_name = line[1]
    columns = line[2:]
    tables[table_name] = {"columns": columns, "data": []}
    print('#' * 22 + ' CREATE ' + '#' * 22)
    print(f'Table {table_name} created with columns: {columns}')
    print('#' * 52)
    print()
    return tables

def insert(line, table_name, tables):
    print('#' * 22 + ' INSERT ' + '#' * 22)
    try:
        if table_name not in tables:
            raise KeyError

        values = line[2:]
        tables[table_name]["data"].append(values)
        values_str = ', '.join([f'"{value}"' for value in values])
        print(f'Inserted into {table_name}: ({values_str})')
        print(f'Table: {table_name}')
        columns = tables[table_name]["columns"]
        print_table(columns, tables[table_name]["data"])
        return tables

    except KeyError:
        print(f'Table {table_name} not found')
        values = list(line[2:])
        tables[table_name]["data"].append(values)
        values_str = ', '.join([f'"{value}"' for value in values])
        print(f'Inserted into {table_name}: ({values_str})')

    print('#' * 52)
    print()

def select(line, table_name, tables):
    print('#' * 22 + ' SELECT ' + '#' * 22)
    condition_dict={}
    try:
        if table_name not in tables:
            raise KeyError

        if 'WHERE' in line:
            select_columns = line[1:line.index('WHERE')]
            conditions_raw = line[line.index('WHERE') + 1:]
            condition_str = ' '.join(conditions_raw).replace('{', '').replace('}', '').replace("'", "")
            conditions = condition_str.split(',')

            for condition in conditions:
                key, value = condition.split(':')
                condition_dict[key] = value

            for col in select_columns:
                if col not in tables[table_name]["columns"]:
                    raise ValueError(f"Column {col} does not exist")

            result = []
            for row in tables[table_name]["data"]:
                match = True
                for key, value in condition_dict.items():
                    if row[tables[table_name]["columns"].index(key)] != value:
                        match = False
                        break

                if match:
                    selected_row = [row[tables[table_name]["columns"].index(col)] for col in select_columns]
                    result.append(selected_row)
            if not result:
                result=None

            print(f'Condition: {condition_dict}')
            print(f'Select result from {table_name}: {result}')



    except KeyError:

        print(f"Table {table_name} not found")

        print(f"Condition: {condition_dict}")

        print(f"Select result from '{table_name}': None")

    except ValueError as e:
        print(e)
        print(f"Condition: {condition_dict}")
        print(f"Select result from '{table_name}': None")


    print('#' * 52)
    print()


def update(line, table_name, tables):
    print('#' * 22 + ' UPDATE ' + '#' * 22)
    updated_count=0
    try:

        if table_name not in tables:
            raise KeyError

        update_values_str = line[2].replace("{", "").replace("}", "").replace("'", "").split(',')
        update_values = {}
        for item in update_values_str:
            key, value = item.split(':')
            update_values[key] = value

        condition_str = line[4].replace("{", "").replace("}", "").replace("'", "").split(':')
        cond_col = condition_str[0]
        cond_val = condition_str[1]

        if cond_col not in tables[table_name]["columns"]:
            raise ValueError


        for row in tables[table_name]["data"]:
            if row[tables[table_name]["columns"].index(cond_col)] == cond_val:
                for update_col, update_val in update_values.items():
                    row[tables[table_name]["columns"].index(update_col)] = update_val
                updated_count += 1

        if updated_count == 0:
            print(f"0 rows updated.")

        print(f"Updated '{table_name}' with {update_values} where {{'{cond_col}': '{cond_val}'}}")
        print(f'{updated_count} rows updated.')
        print()
        print(f'Table: {table_name}')
        print_table(tables[table_name]["columns"], tables[table_name]["data"])


        return tables

    except KeyError:
        try:

            update_values = line[2].replace("{", "").replace("}", "").replace("'", "").split(',')
            update_values_dict = {}
            for item in update_values:
                key, value = item.split(':')
                update_values_dict[key] = value

            condition_str = line[4].replace("{", "").replace("}", "").replace("'", "").split(':')
            cond_col = condition_str[0]
            cond_val = condition_str[1]
            print(f"Updated '{table_name}' with {update_values_dict} where {{'{cond_col}': '{cond_val}'}}")
            print(f'Table {table_name} not found')
            print(f"{updated_count} rows updated.")
        except:
            return None

    except ValueError:
        update_values_str = line[2].replace("{", "").replace("}", "").replace("'", "").split(',')
        update_values_dict = {}
        for item in update_values_str:
            key, value = item.split(':')
            update_values_dict[key] = value

        condition_str = line[4].replace("{", "").replace("}", "").replace("'", "").split(':')
        cond_col = condition_str[0]
        cond_val = condition_str[1]
        print(f"Updated '{table_name}' with {update_values_dict} where {{'{cond_col}': '{cond_val}'}}")
        print(f'Column {cond_col} does not exist')
        print(f'{updated_count} rows updated')
        print()
        print_table(tables[table_name]["columns"], tables[table_name]["data"])


    print('#' * 52)
    print()


def delete(line, table_name, tables):
    print('#' * 22 + ' DELETE ' + '#' * 22)

    deleted_count=0
    try:
        if table_name not in tables:
            raise KeyError

        condition_str = line[2].replace("{", "").replace("}", "").replace("'", "").split(':')
        cond_col = condition_str[0]
        cond_val = condition_str[1]

        if cond_col not in tables[table_name]["columns"]:
            raise ValueError

        initial_count = len(tables[table_name]["data"])
        new_data = [row for row in tables[table_name]["data"]
                    if row[tables[table_name]["columns"].index(cond_col)] != cond_val]

        deleted_count = initial_count - len(new_data)
        tables[table_name]["data"] = new_data

        print(f"Deleted from '{table_name}' where {{'{cond_col}': '{cond_val}'}}")
        print(f'{deleted_count} rows deleted.')
        print()
        print(f'Table: {table_name}')
        print_table(tables[table_name]["columns"], tables[table_name]["data"])

    except KeyError:
        condition_str = line[2].replace("{", "").replace("}", "").replace("'", "").split(':')
        cond_col = condition_str[0]
        cond_val = condition_str[1]
        print(f"Deleted from '{table_name}' where {{'{cond_col}': '{cond_val}'}}")
        print(f"Table {table_name} not found")
        print(f'{deleted_count} rows deleted.')
    except ValueError:
        condition_str = line[2].replace("{", "").replace("}", "").replace("'", "").split(':')
        cond_col = condition_str[0]
        cond_val = condition_str[1]
        print(f"Deleted from '{table_name}' where {{'{cond_col}': '{cond_val}'}}")
        print(f"Column {cond_col} does not exist")
        print(f'{deleted_count} rows deleted.')
        print()
        print(f'Table: {table_name}')
        print_table(tables[table_name]["columns"], tables[table_name]["data"])



    print('#' * 52)
    print()
    return tables



def count(line, table_name, columns,tables):
    print('#' * 22 + ' COUNT ' + '#' * 22)
    num_count = 0
    if 'WHERE' in line:
        line_cond = line[line.index('WHERE') + 1:]
        line_cond_str = ' '.join(line_cond).replace('{', '').replace('}', '').replace("'", "")
        cond_col, cond_val = line_cond_str.split(':')
        for row in tables[table_name]['data']:
            if row[columns.index(cond_col)] == cond_val:
                num_count += 1

    print(f'Count: {num_count}')
    print(f'Total number of entries in {table_name} is {num_count}')
    print('#' * 52)
    print()

def join(line,tables):
    table1_name, table2_name = line[1].split(',')
    join_column = line[line.index("ON") + 1]

    table1 = tables[table1_name]
    table2 = tables[table2_name]

    table1_columns = table1["columns"]
    table2_columns = table2["columns"]

    table1_join_index = table1_columns.index(join_column)
    table2_join_index = table2_columns.index(join_column)

    new_columns = table1_columns + table2_columns

    new_data = []
    for row1 in table1["data"]:
        for row2 in table2["data"]:
            if row1[table1_join_index] == row2[table2_join_index]:
                new_row = row1 + row2
                new_data.append(new_row)

    print(f'Join tables {table1_name} and {table2_name}')
    print('Table: Joined Table')
    print_table(new_columns, new_data)
    print('#' * 52)
    print()


def main():
    input_file = sys.argv[1]

    with open(input_file, 'r') as file:
        datas = file.readlines()

    tables = {}

    for line in datas:
        line = line.split()

        if line[0] == "CREATE_TABLE":
            tables = create(line, tables)

        elif line[0] == 'INSERT':
            table_name = line[1]
            tables = insert(line, table_name, tables)

        elif line[0] == 'SELECT':
            table_name = line[1]
            select(line, table_name, tables[table_name]["columns"])

        elif line[0] == 'UPDATE':
            table_name = line[1]
            tables = update(line, table_name, tables[table_name]["columns"])

        elif line[0] == 'DELETE':
            table_name = line[1]
            tables = delete(line, table_name, tables[table_name]["columns"])

        elif line[0] == 'COUNT':
            table_name = line[1]
            count(line, table_name, tables[table_name]["columns"], tables)

if __name__ == "__main__":
    main()
