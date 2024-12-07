from eralchemy import render_er
from sqlalchemy import create_engine

# Database configuration
DATABASE_CONFIG = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'port': 3306,
    'database': 'your_database_name',
}


def generate_erd():
    # Create database connection string
    db_url = f"mysql+pymysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

    # Generate ERD
    output_file = 'erd_diagram.png'  # Output file name
    render_er(db_url, output_file)
    print(f"ERD diagram saved as {output_file}")


if __name__ == "__main__":
    generate_erd()
