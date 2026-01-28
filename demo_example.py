#!/usr/bin/env python3
"""
Demo script showing how to use the generated Google API Python code.
This demonstrates the Google Example Library API.
"""

import sys
import os

# Add the output directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'output'))

try:
    from google.example.library.v1 import library_pb2
    from google.protobuf import empty_pb2
    
    print("✅ Successfully imported generated Google API code!")
    print()
    
    # Demonstrate creating a Book message
    print("📚 Creating a Book message:")
    book = library_pb2.Book()
    book.name = "shelves/1/books/123"
    book.author = "Jane Doe"
    book.title = "The Great Adventure"
    book.read = True
    
    print(f"  - Name: {book.name}")
    print(f"  - Author: {book.author}")
    print(f"  - Title: {book.title}")
    print(f"  - Read: {book.read}")
    print()
    
    # Demonstrate creating a Shelf message
    print("📖 Creating a Shelf message:")
    shelf = library_pb2.Shelf()
    shelf.name = "shelves/1"
    shelf.theme = "Fiction"
    
    print(f"  - Name: {shelf.name}")
    print(f"  - Theme: {shelf.theme}")
    print()
    
    # Demonstrate creating service requests
    print("🔧 Creating service request examples:")
    
    # Create Shelf Request
    create_shelf_req = library_pb2.CreateShelfRequest()
    create_shelf_req.shelf.CopyFrom(shelf)
    print(f"  - CreateShelfRequest: {create_shelf_req}")
    
    # Get Book Request
    get_book_req = library_pb2.GetBookRequest()
    get_book_req.name = "shelves/1/books/123"
    print(f"  - GetBookRequest.name: {get_book_req.name}")
    
    print()
    print("🎉 Demo completed successfully!")
    print()
    print("Available message types in library_pb2:")
    for attr in dir(library_pb2):
        if not attr.startswith('_') and hasattr(getattr(library_pb2, attr), 'DESCRIPTOR'):
            print(f"  - {attr}")
            
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure the output directory contains the generated Python code.")
except Exception as e:
    print(f"❌ Error: {e}")
