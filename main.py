import mysql.connector
import fastapi
import fastapi.middleware.cors

app = fastapi.FastAPI()
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

class Managerdb:
    def __init__(self, host, user, password, database):
        self.mydb = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database,
        )
        self.mycursor = self.mydb.cursor()

    def selectdb(self, table):
        sql = f"SELECT * FROM {table}"
        self.mycursor.execute(sql)
        columes = [dese[0] for dese in self.mycursor.description]
        show = self.mycursor.fetchall()
        return columes, show
    
    def deletedb(self, table, id_name, id):
        sql = f"DELETE FROM {table} WHERE {id_name} = %s"
        val_sql = (id,)
        self.mycursor.execute(sql, val_sql)
        self.mydb.commit()
        if self.mycursor.rowcount > 0:
            return True
        else:
            return False
    
    def editdb(self, table, colum, id_name, id, val):
        sql = f"UPDATE {table} SET {colum} = %s WHERE {id_name} = %s"
        val_sql = (val, id)
        self.mycursor.execute(sql, val_sql)
        self.mydb.commit()
        if self.mycursor.rowcount > 0:
            return True
        else:
            return False
    
    def insert_users(self, username, password, email, user_role):
        sql = "INSERT INTO users VALUES (%s, %s, %s, %s, %s)"
        val_sql = (None, username, password, email, user_role)
        self.mycursor.execute(sql, val_sql)
        self.mydb.commit()
        if self.mycursor.rowcount > 0:
            return True
        else:
            return False
        
    def insert_products(self, product_name, description, price, stock, category_id):
        sql = "INSERT INTO products VALUES (%s, %s, %s, %s, %s, %s)"
        val_sql = (None, product_name, description, price, stock, category_id)
        self.mycursor.execute(sql, val_sql)
        self.mydb.commit()
        if self.mycursor.rowcount > 0:
            return True
        else:
            return False
    
    def insert_categories(self, categories_name):
        sql = "INSERT INTO categories VALUES (%s, %s)"
        val_sql = (None, categories_name)
        self.mycursor.execute(sql, val_sql)
        self.mydb.commit()
        if self.mycursor.rowcount > 0:
            return True
        else:
            return False
        
    def insert_orders(self, user_id, order_date, total_amount, status, product_id):
        sql = "INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s)"
        val_sql = (None, user_id, order_date, total_amount, status, product_id)
        self.mycursor.execute(sql, val_sql)
        self.mydb.commit()
        if self.mycursor.rowcount > 0:
            return True
        else:
            return False

db = {
    'shop_db' : Managerdb("localhost", "root", "1234", "shop")
}

#http://localhost:8000/selectdb/shop_db/users

@app.get("/selectdb/{database}/{table}")
async def select_db(database, table):
    all_db = db[database]
    columns, result = all_db.selectdb(table)
    pun = [dict(zip(columns, row)) for row in result]
    return {"select_data": pun}

@app.get("/deletedb/{database}/{table}/{id_name}/{id}")
async def delete_db(database, table, id_name, id):
    all_db = db[database]
    result = all_db.deletedb(table, id_name, id)
    return {"delete_data": result}

@app.get("/editdb/{database}/{table}/{column}/{id_name}/{id}/{val}")
async def edit_db(database, table, column, id_name, id, val):
    all_db = db[database]
    result = all_db.editdb(table, column, id_name, id, val)
    return {"edit_data": result}
    
@app.get("/insert_users/{database}/{username}/{password}/{email}/{user_role}")
async def insert_users(database, username, password, email, user_role):
    all_db = db[database]
    result = all_db.insert_users(username, password, email, user_role)
    return {"insert_users_data": result}

@app.get("/insert_products/{database}/{product_name}/{description}/{price}/{stock}/{category_id}")
async def insert_porducts(database, product_name, description, price, stock, category_id):
    all_db = db[database]
    result = all_db.insert_products(product_name, description, price, stock, category_id)
    return {"insert_products_data": result}

@app.get("/insert_categories/{database}/{categories_name}")
async def insert_categories(database, categories_name):
    all_db = db[database]
    result = all_db.insert_categories(categories_name)
    return {"insert_categories_data": result}

@app.get("/insert_orders/{database}/{user_id}/{order_date}/{total_amount}/{status}/{product_id}")
async def insert_orders(database, user_id, order_date, total_amount, status, product_id):
    all_db = db[database]
    result = all_db.insert_orders(user_id, order_date, total_amount, status, product_id)
    return {"insert_orders_data": result}