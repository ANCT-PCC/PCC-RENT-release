import dbc

allusers = dbc.get_all_users()

for row in allusers:
    prev_grade = int(row[9][:1])
    new_grade = prev_grade+1
    dbc.update_user_info(row[1],'grade',str(new_grade)+'年 ')