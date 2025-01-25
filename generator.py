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
import json


class Generator:

    def __init__(self, file_path: str):
        self.file = file_path
        self.db = {}
        self.db["imports"] = {"sqlalchemy": set([])} # add here any module u will need in future generationo
    
    def _add_new_import(self, module: str, importing: str):
        self.db["imports"]["sqlalchemy"].add(importing)
    def _parse_col_type(self, col_type: str):
        if col_type == "integer":
            self._add_new_import("sqlalchemy", "Integer")
            return "Integer"
        if "varchar" in col_type:
            self._add_new_import("sqlalchemy", "String")
            return "String({})".format(re.search(r'varchar\((\d+)\)', col_type).group(1))

    def _sql_file_reader(self) -> dict:
        def obtain_table_name(cad): return cad.split(" ")[2].strip()
        with open(self.file, 'r') as file:
            for line in file:
                if "CREATE TABLE" in line:
                    table_name = obtain_table_name(line)
                    self.db[table_name] = {}
                    file.readline()
                    for line in file:
                        if line.startswith(');'):
                            break
                        if "PRIMARY KEY" in line:  # assumes that all cols has been already read
                            # guarrada mirar como hacer mejor
                            p_keys = line[15:-2].split(', ')
                            for key in p_keys:
                                self.db[table_name][key].append("primary_key=True")
                        else:
                            splitted_col_line = line.split()
                            col_name = splitted_col_line[0]
                            col_type = splitted_col_line[1]
                            nullable = True if splitted_col_line[2] != "NOT" else False
                            attribs = [self._parse_col_type(col_type)]
                            if not nullable:
                                attribs.append("nullable=False")
                            self.db[table_name][col_name] = attribs
                            

                # just understands foreign key with ids of other tables (just useful for intersection tables)
                if "ALTER TABLE" in line:
                    table_name = obtain_table_name(line)
                    splitted_fk = file.readline().split()[2].split('_')
                    to_index = splitted_fk.index('TO')
                    first_table = '_'.join(splitted_fk[1:to_index])
                    second_table = '_'.join(splitted_fk[to_index+1:])
                    self.db[second_table][first_table +"_id"].append("ForeignKey(" + first_table + ".id)")
            
            # TODO: checks if there is any table with 2 primary keys so that property should be deleted
            # an added a composed primary key constraint with those variables
            

    def _build_models(self):
        '''
        builds all sqlalchemy models 
        in the model folder
        '''
        ident = 1
        blanks = "".join([" " for i in range(4 * ident)])
        imports = """
        from ..config.db.databse_setup import Base
        from sqlalchemy import sqlalchemyimports 
        """
        usedSQLalchemyImports = []
        def take_varchar_len(x): return int(
            re.search(r'varchar\((\d+)\)', x).group(1))
        
        # 2.  create the rest of files
        for tablename, cols in self.db.items():
            with open(tablename + '.py', 'w') as file:
                # Create sql Model
                classFormatedName = ''.join(
                    [tok.capitalize() for tok in tablename.split('_')])
                file.write(f"class {classFormatedName}(Base):\n")
                for col, col_attribs in cols.items():
                    sqlalchemy_col = blanks + f"{col} = Column("
                    for i in range(len(col_attribs)):
                        sqlalchemy_col += col_attribs[i]
                        if i != len(col_attribs) - 1:
                            sqlalchemy_col += ", "
                    sqlalchemy_col += ")\n"
                    file.write(sqlalchemy_col)
                file.write("")

        # 3. adding import to sqlalchemy model file

    def generateFastAPItemplate(self):
        self._sql_file_reader()
        print(self.db)
        self._build_models()


if __name__ == '__main__':
    gen = Generator(sys.argv[1])
    gen.generateFastAPItemplate()
