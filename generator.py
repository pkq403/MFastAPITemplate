'''
proyect generated structure in proyectstructure.txt file
python3 generator.py path-to-gen-project
it generates reading a .sql file with db 
(generate it by using ERD editor 2.0.4 VS Code extension)
IMPORTANT:
names of the tables should be always singular in order to make this
script work, the foreign key cols should be always <table-name>_id
'''
import sys
import re
import os
import json


class Generator:

    def __init__(self, file_path: str, project_path: str):
        self.db = {}
        self.file = file_path
        self.proyect_path  = project_path
        # Dynamic content
        self.api_path = os.path.join(project_path, 'api')
        self.controllers_path = os.path.join(project_path, self.api_path, 'controllers')
        self.schemas_path = os.path.join(project_path, 'schemas')
        self.models_path = os.path.join(project_path, 'models')
        self.repos_paht = os.path.join(project_path, 'repositories')
        # Static content (config, auth, tests...)

        
    
    def _add_new_import(self, table: str,  module: str, importing: str):
        self.db[table]["imports"][module].add(importing)

    def _parse_col_type(self, tablename: str, col_type: str):
        if col_type == "integer":
            self._add_new_import(tablename, "sqlalchemy", "Integer")
            return "Integer"
        if "varchar" in col_type:
            self._add_new_import(tablename, "sqlalchemy", "String")
            return "String({})".format(re.search(r'varchar\((\d+)\)', col_type).group(1))

    def _sql_file_reader(self) -> dict:
        def obtain_tablename(cad): return cad.split(" ")[2].strip()
        with open(self.file, 'r') as file:
            for line in file:
                if "CREATE TABLE" in line:
                    tablename = obtain_tablename(line)
                    self.db[tablename] = {}
                    self.db[tablename]["imports"] = {"sqlalchemy": set(["Column"])}
                    file.readline()
                    for line in file:
                        if line.startswith(');'):
                            break
                        if "PRIMARY KEY" in line:  # assumes that all cols has been already read
                            # guarrada mirar como hacer mejor
                            p_keys = line[15:-2].split(', ')
                            for key in p_keys:
                                self.db[tablename][key].append("primary_key=True")
                        else:
                            splitted_col_line = line.split()
                            col_name = splitted_col_line[0]
                            col_type = splitted_col_line[1]
                            nullable = True if splitted_col_line[2] != "NOT" else False
                            attribs = [self._parse_col_type(tablename, col_type)]
                            if not nullable:
                                attribs.append("nullable=False")
                            self.db[tablename][col_name] = attribs
                            

                # just for foreign key with ids of other tables (just useful for intersection tables)
                if "ALTER TABLE" in line:
                    tablename = obtain_tablename(line)
                    splitted_fk = file.readline().split()[2].split('_')
                    to_index = splitted_fk.index('TO')
                    first_table = '_'.join(splitted_fk[1:to_index])
                    second_table = '_'.join(splitted_fk[to_index+1:])
                    self.db[second_table][first_table +"_id"].append("ForeignKey(" + first_table + ".id)")
            
            for tablename in self.db:
                table = self.db[tablename]
                pk = [col for col in table if "primary_key=True" in table[col]]
                if len(pk) > 1:
                    pk_constaint_str = "PrimaryKeyConstraint("
                    for k in pk:
                        pk_constaint_str += k.replace('_', '.') + ','
                    table['__table_args__'] = [pk_constaint_str[:-1] + ')']

    def _build_models(self):
        '''
        builds all sqlalchemy models 
        in the model folder
        '''
        ident = 1
        blanks = "".join([" " for i in range(4 * ident)])
        # 1. create models dir
        os.makedirs(self.models_path, exist_ok=True)
        # 2.  create the rest of files
        for tablename, cols in self.db.items():
            writelines = []
            # Create sql Model
            classFormatedName = ''.join(
                [tok.capitalize() for tok in tablename.split('_')])
            writelines.append(f"class {classFormatedName}(Base):\n")
            for col, col_attribs in cols.items():
                if col == "imports":
                    continue 
                if col == "__table_args__":
                    writelines.append("\n")
                sqlalchemy_col = blanks + f"{col} = Column("
                for i in range(len(col_attribs)):
                    sqlalchemy_col += col_attribs[i]
                    if i != len(col_attribs) - 1:
                        sqlalchemy_col += ", "
                sqlalchemy_col += ")\n"
                writelines.append(sqlalchemy_col)
            table_imports = []
            for i, module in enumerate(cols["imports"]):
                import_lst = ', '.join(cols["imports"][module])
                import_str = f"from {module} import {import_lst}\n"
                if i == len(cols["imports"]) - 1: # dirty, no need to check every iteration, lazy, look to improve
                    import_str+='\n'
                writelines.insert(0,import_str)

            with open(os.path.join(self.models_path, tablename + '.py'), 'w') as file:
                file.writelines(writelines)

    def generateFastAPItemplate(self):
        self._sql_file_reader()
        print(self.db)
        self._build_models()


if __name__ == '__main__':
    gen = Generator(sys.argv[1], sys.argv[2])
    gen.generateFastAPItemplate()
