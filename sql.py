from python_helpers import execute_sql

def drop_table(table_name):
    # this is an example of using the f format for execute sql.
    # you don't need to do anything here.
    execute_sql(f'DROP table if exists {table_name};', debug = True)
    # an example with values:
    # execute_sql('a valid sql statement with (%s, %s) arguments;)' values = [2,'two'])
    # renders: 'a valid sql statement with (2, 'two') arguments;)

def create_tables():
    # PLEASE NOTE THE REST OF THE FUNCTIONS DO NOT RELY ON THIS.
    # IF IT IS FIGHTING YOU, MOVE ON. YOU CAN PASS WITHOUT IT.

    # create a table named hotels
    #   fields:
    #       id (primary id autoincrment)
    #       name (uniqe varchar)
    #       number_of_rooms (an integer)
    #       number_of_stories (an integer)
    #       has_pool (a boolean) [1 or 0]
    #       has_gym (a boolean) [1 or 0]
    
    create_hotel_table_sql = '''
    CREATE TABLE hotels (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        number_of_rooms INT NOT NULL,
        number_of_stories INT NOT NULL,
        has_pool BOOLEAN NOT NULL,
        has_gym BOOLEAN NOT NULL
    );
    '''
    execute_sql(create_hotel_table_sql, debug = False)

    # create a table named rooms
    #   fields:
    #       id (primary id autoincrement)
    #       number (integer)
    #       price (integer)
    #       occupied (a boolean) [1 or 0]
    #       needs_cleaning (a boolean) [1 or 0]
    
    create_rooms_table_sql = '''
    CREATE TABLE rooms (
        id INT AUTO_INCREMENT PRIMARY KEY,
        number INT NOT NULL,
        price INT NOT NULL,
        occupied BOOLEAN DEFAULT FALSE,
        needs_cleaning BOOLEAN DEFAULT FALSE,
        hotel_id INT,
        FOREIGN KEY (hotel_id) REFERENCES hotels(id)
    );
    '''
    execute_sql(create_rooms_table_sql, debug = False)

def insert_hotel(name,number_of_rooms, number_of_stories,has_pool, has_gym):
    # insert a hotel into the hotels table using the values above
    insert_hotel_sql = '''
    INSERT INTO hotels (name, number_of_rooms, number_of_stories, has_pool, has_gym)
    VALUES (%s, %s, %s, %s, %s);
    '''

    #execute_sql(insert_hotel_sql, debug = False)
    #or the below with values populated
    #execute_sql(insert_hotel_sql, values = [], debug = False)
    execute_sql(insert_hotel_sql, values = [name, number_of_rooms, number_of_stories, has_pool, has_gym], debug=True)

def insert_room(hotel_id, number, price, occupied = False, needs_cleaning = False):
    insert_room_sql =  '''
    INSERT INTO rooms (hotel_id, number, price, occupied, needs_cleaning)
    VALUES (%s, %s, %s, %s, %s);
    '''
    
    execute_sql(insert_room_sql, values=[hotel_id, number, price, occupied, needs_cleaning], debug = True)


def get_hotel_id_from_name(name):
    # this function should return the id of the matching hotel.
    get_sql = 'SELECT id FROM hotels WHERE name = %s;'
    result = execute_sql(get_sql, values = [name], debug = True)
    # check that result is an integer and not a list or a tuple.
    return result[0][0] if result else None

def get_available_rooms(hotel_id, price):
    # Goal: return a list of available room numbers at the hotel_id with a price less than or equal to price.
    get_sql = '''
    SELECT number FROM rooms
    WHERE hotel_id = %s AND price <= %s AND occupied = FALSE;
    '''
    query_results = execute_sql(get_sql, values=[hotel_id, price], debug = True)
    # check that results is a list of integers if it isn't make it so it is, you may need to use a for loop
    # on query_results.
    return [row[0] for row in query_results]

def checkout_room(hotel_id, room_number):
    # update the status of the room to occupied = 1.
    # update the status of the room to needs_cleaning = 1.
    # !NOTE the table rooms has a field named number not room_number
    update_sql = '''
    UPDATE rooms
    SET occupied = TRUE, needs_cleaning = TRUE
    WHERE hotel_id = %s AND number = %s
    '''
    execute_sql(update_sql, values = [hotel_id, room_number], debug=True)

def makeover_room(hotel_id, room_number):
    # update the status of the room to occupied = 0
    # update the status of the room to needs_cleaning = 0.
    # !NOTE the table rooms has a field named number not room_number
    update_sql = '''
    UPDATE rooms
    SET occupied = FALSE, needs_cleaning = FALSE
    WHERE hotel_id = %s AND number = %s;
    '''
    execute_sql(update_sql, values = [hotel_id, room_number], debug=True)


if __name__ == "__main__":
    
    drop_table('hotels')
    drop_table('rooms')

    explore = False # set explore to true to run this main test.
    create_tables()
    if explore:
        create_tables()
        insert_hotel('Apple',12,3,0, 0)
        apple_id = get_hotel_id_from_name('Apple')
        print(apple_id)
        insert_room(apple_id, 101, 80)
        available_rooms = get_available_rooms(apple_id, 200)
        print(x)
        checkout_room(apple_id,101)
        print(execute_sql('select * from rooms;'))
        makeover_room(apple_id,101)
        print(execute_sql('select * from rooms;'))