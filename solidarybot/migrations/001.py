def forward(cursor):
    cursor.execute("""
            CREATE TABLE solidary (
                id INTEGER PRIMARY KEY autoincrement,
                hashtag text,
                sum text default '0',
                maxsum text,
                person text default '',
                private text default 'False',
                end text default 'False'
            )
    """)