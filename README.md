# 🔗 URL Shortener

A simple command-line URL shortener that creates shortened URLs and stores them locally.

## ✨ Features

- 🔹 Shorten long URLs to easy-to-share short links
- 🔍 Expand shortened URLs to their original form
- 📋 List all shortened URLs in the database
- ❌ Delete shortened URLs when no longer needed
- 🎯 Create custom short codes for memorable links
- 💾 Store all URLs in a local JSON database

## 🔧 Requirements

- Python 3.6 or higher

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xAp0llo/url-shortener.git
cd url-shortener
```

2. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage
```bash
python main.py <command> [options]
```

## ⚙️ Commands

- `shorten`: Shorten a URL
expand: Expand a shortened URL
list: List all shortened URLs
delete: Delete a shortened URL

## 📝 Examples

Shorten a URL:
```bash
python main.py shorten https://www.example.com/very/long/path/to/resource
```

Use a custom short code:
```bash
python main.py shorten https://www.example.com -c example123
```

Expand a shortened URL:
```bash
python main.py expand Abc123
```
or
```bash
python main.py expand http://short.url/Abc123
```

List all shortened URLs:
```bash
python main.py list
```

Delete a shortened URL:
```bash
python main.py delete Abc123
```
or
```bash
python main.py delete http://short.url/Abc123
```

## 📄 Notes

The base URL (http://short.url/) is just a placeholder. In a real-world application, you would replace this with your actual domain.
All shortened URLs are stored locally in a JSON file (urls.json by default).
To make this a fully functional web service, you would need to deploy it with a web framework like Flask or FastAPI.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
