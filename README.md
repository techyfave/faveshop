# 🛍️ FaveShop - Django Ecommerce Platform
FaveShop is a modern, full-featured ecommerce website built with Django that provides users with a complete online shopping experience.

## ✨ Features
## 🛒 Shopping Features
- **Product Catalog** - Browse products by categories with search functionality

- **Shopping Cart** - Add, update, and remove items with real-time calculations

- **Product Reviews** - Users can rate and review products

- **Responsive Design** - Mobile-friendly interface built with Bootstrap 5

## 👤 User Features
- Secure user registration and authentication

- User profile management

- Product review system

- Shopping cart persistence

## 🏪 Admin Features
- Django admin interface for managing products, categories, and reviews

- Product inventory management

- User management

## 🏗️ Tech Stack

### Backend
- Python 3.13+

- Django 4.2+

- Django REST Framework

- SQLite/PostgreSQL

### Frontend
- HTML5/CSS3

- Bootstrap 5

- JavaScript

### Tools
- Pillow (Image processing)

- Crispy Forms (Form styling)

## 🚀 Quick Start
### Prerequisites
- Python 3.13 or higher

- pip package manager

### Installation
1. **Clone and navigate**

```bash
git clone https://github.com/yourusername/faveshop.git
cd faveshop
```
2. **Setup virtual environment**

``` bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
3. **Install requirements**

```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy environment file
cp .env.example .env
# Edit .env with your settings
```
5. **Setup database**

```bash
python manage.py migrate
python manage.py createsuperuser
```
6. **Run development server**

```bash
python manage.py runserver
Visit http://127.0.0.1:8000 to start shopping!
```

## 📁 Project Structure
```text
faveshop/
├── accounts/          # User authentication
├── cart/             # Shopping cart functionality  
├── orders/            # order info  
├── pages/            # Static pages including homepage
├── products/         # Product catalog, categories, reviews
└── templates/        # HTML templates
```

## 📞 Support
For questions or support, please contact the development team.

Happy Shopping with FaveShop! 🛍️
