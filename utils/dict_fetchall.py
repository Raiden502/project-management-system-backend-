def dictfetchall(cursor):
    columns = [col for col in cursor.keys()]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]