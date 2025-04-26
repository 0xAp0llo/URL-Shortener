#!/usr/bin/env python3

import random
import string
import argparse
import json
import os
import re
from urllib.parse import urlparse

# Constants
DEFAULT_DB_FILE = "urls.json"
DEFAULT_SHORT_LENGTH = 6
BASE_URL = "http://short.url/"  # This is just a placeholder

def is_valid_url(url):
    """Validate if the provided string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def generate_short_code(length=DEFAULT_SHORT_LENGTH):
    """Generate a random short code of specified length"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def load_database(db_file=DEFAULT_DB_FILE):
    """Load URL database from file"""
    if os.path.exists(db_file):
        try:
            with open(db_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {db_file} is corrupted. Creating a new database.")
            return {"urls": {}, "reverse": {}}
    return {"urls": {}, "reverse": {}}

def save_database(db, db_file=DEFAULT_DB_FILE):
    """Save URL database to file"""
    with open(db_file, 'w') as f:
        json.dump(db, f, indent=4)

def shorten_url(long_url, db_file=DEFAULT_DB_FILE, length=DEFAULT_SHORT_LENGTH, custom_code=None):
    """Shorten a URL and store it in the database"""
    # Validate URL
    if not is_valid_url(long_url):
        print(f"Error: '{long_url}' is not a valid URL")
        return None

    # Load database
    db = load_database(db_file)
    
    # Check if URL already exists in database
    if long_url in db["reverse"]:
        short_code = db["reverse"][long_url]
        print(f"URL already shortened: {BASE_URL}{short_code}")
        return f"{BASE_URL}{short_code}"
    
    # Generate or use custom short code
    if custom_code:
        if custom_code in db["urls"]:
            print(f"Error: Custom code '{custom_code}' is already in use")
            return None
        short_code = custom_code
    else:
        # Generate a unique short code
        while True:
            short_code = generate_short_code(length)
            if short_code not in db["urls"]:
                break
    
    # Add to database
    db["urls"][short_code] = long_url
    db["reverse"][long_url] = short_code
    
    # Save database
    save_database(db, db_file)
    
    # Return shortened URL
    shortened_url = f"{BASE_URL}{short_code}"
    print(f"Shortened URL: {shortened_url}")
    return shortened_url

def expand_url(short_code, db_file=DEFAULT_DB_FILE):
    """Expand a short URL code to its original URL"""
    # Load database
    db = load_database(db_file)
    
    # Check if short code exists
    if short_code in db["urls"]:
        long_url = db["urls"][short_code]
        print(f"Original URL: {long_url}")
        return long_url
    else:
        print(f"Error: Short code '{short_code}' not found")
        return None

def list_urls(db_file=DEFAULT_DB_FILE):
    """List all shortened URLs in the database"""
    # Load database
    db = load_database(db_file)
    
    if not db["urls"]:
        print("No URLs in the database")
        return
    
    print("\n" + "="*70)
    print(f"{'Short URL':<20} | {'Original URL':<48}")
    print("="*70)
    
    for short_code, long_url in db["urls"].items():
        short_url = f"{BASE_URL}{short_code}"
        # Truncate long URLs for display
        displayed_url = long_url
        if len(displayed_url) > 48:
            displayed_url = displayed_url[:45] + "..."
        print(f"{short_url:<20} | {displayed_url:<48}")
    
    print("="*70)
    print(f"Total: {len(db['urls'])} URLs")
    print("="*70 + "\n")

def delete_url(short_code, db_file=DEFAULT_DB_FILE):
    """Delete a shortened URL from the database"""
    # Load database
    db = load_database(db_file)
    
    # Check if short code exists
    if short_code in db["urls"]:
        long_url = db["urls"][short_code]
        
        # Remove from database
        del db["urls"][short_code]
        del db["reverse"][long_url]
        
        # Save database
        save_database(db, db_file)
        
        print(f"Deleted: {BASE_URL}{short_code} -> {long_url}")
        return True
    else:
        print(f"Error: Short code '{short_code}' not found")
        return False

def parse_short_code(url):
    """Extract short code from a shortened URL"""
    match = re.search(r'\/([a-zA-Z0-9]+)$', url)
    return match.group(1) if match else url

def main():
    parser = argparse.ArgumentParser(description="Simple URL Shortener")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Shorten command
    shorten_parser = subparsers.add_parser("shorten", help="Shorten a URL")
    shorten_parser.add_argument("url", help="URL to shorten")
    shorten_parser.add_argument("-l", "--length", type=int, default=DEFAULT_SHORT_LENGTH, help=f"Length of short code (default: {DEFAULT_SHORT_LENGTH})")
    shorten_parser.add_argument("-c", "--custom", help="Custom short code")
    shorten_parser.add_argument("-d", "--database", default=DEFAULT_DB_FILE, help=f"Database file (default: {DEFAULT_DB_FILE})")
    
    # Expand command
    expand_parser = subparsers.add_parser("expand", help="Expand a shortened URL")
    expand_parser.add_argument("code", help="Short code or URL to expand")
    expand_parser.add_argument("-d", "--database", default=DEFAULT_DB_FILE, help=f"Database file (default: {DEFAULT_DB_FILE})")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all shortened URLs")
    list_parser.add_argument("-d", "--database", default=DEFAULT_DB_FILE, help=f"Database file (default: {DEFAULT_DB_FILE})")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a shortened URL")
    delete_parser.add_argument("code", help="Short code or URL to delete")
    delete_parser.add_argument("-d", "--database", default=DEFAULT_DB_FILE, help=f"Database file (default: {DEFAULT_DB_FILE})")
    
    args = parser.parse_args()
    
    if args.command == "shorten":
        shorten_url(args.url, args.database, args.length, args.custom)
    elif args.command == "expand":
        short_code = parse_short_code(args.code)
        expand_url(short_code, args.database)
    elif args.command == "list":
        list_urls(args.database)
    elif args.command == "delete":
        short_code = parse_short_code(args.code)
        delete_url(short_code, args.database)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
