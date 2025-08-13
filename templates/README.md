# 💰 Personal Finance Tracker

A modern, full-stack web application for tracking personal finances with beautiful visualizations and analytics.

## 🌟 Features

### Core Functionality
- **User Authentication** - Secure registration and login system
- **Transaction Management** - Add, edit, and categorize income/expenses
- **Category System** - Customizable spending categories with color coding
- **Dashboard Overview** - Real-time financial summary and recent transactions
- **Interactive Charts** - Beautiful visualizations using Chart.js
- **Reports & Analytics** - Detailed spending analysis and trends
- **Data Export** - Download transactions as CSV
- **Responsive Design** - Works perfectly on desktop and mobile

### Financial Insights
- Monthly income vs expenses tracking
- Spending breakdown by category
- Financial trends over time
- Savings rate calculation
- Weekly spending patterns
- Personalized recommendations

## 🛠️ Technology Stack

**Backend:**
- **Python Flask** - Web framework
- **SQLite** - Database
- **Werkzeug** - Password hashing and security
- **Gunicorn** - Production WSGI server

**Frontend:**
- **HTML5/CSS3** - Structure and styling
- **Bootstrap 5** - Responsive UI framework
- **JavaScript (ES6)** - Interactive functionality
- **Chart.js** - Data visualization
- **Font Awesome** - Icons

**Deployment:**
- **Render** - Cloud hosting platform
- **GitHub** - Version control and CI/CD

## 🚀 Live Demo

**[View Live Application →](https://personal-finance-tracker-demo.onrender.com)**

**Demo Account:**
- Create your own account or test with any credentials
- All data is isolated per user

## 📱 Screenshots

### Dashboard
![Dashboard Overview](https://via.placeholder.com/800x400/3b82f6/ffffff?text=Dashboard+Overview)

### Transaction Management
![Transaction Management](https://via.placeholder.com/800x400/10b981/ffffff?text=Transaction+Management)

### Analytics & Reports
![Analytics Reports](https://via.placeholder.com/800x400/8b5cf6/ffffff?text=Analytics+%26+Reports)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│                 │    │                 │    │                 │
│ • HTML/CSS/JS   │◄──►│ • Flask API     │◄──►│ • SQLite        │
│ • Bootstrap 5   │    │ • User Auth     │    │ • User Data     │
│ • Chart.js      │    │ • Data Logic    │    │ • Transactions  │
│ • Responsive    │    │ • Route Handlers│    │ • Categories    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `email` - User email
- `password_hash` - Encrypted password
- `created_at` - Registration timestamp

### Categories Table
- `id` - Primary key
- `name` - Category name (Food, Transport, etc.)
- `color` - Hex color for visualization
- `user_id` - Foreign key to users

### Transactions Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `category_id` - Foreign key to categories
- `amount` - Transaction amount
- `description` - Transaction description
- `transaction_type` - 'income' or 'expense'
- `date` - Transaction date
- `created_at` - Entry timestamp

### Budgets Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `category_id` - Foreign key to categories
- `amount` - Budget limit
- `month_year` - Budget period

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/personal-finance-tracker.git
cd personal-finance-tracker
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
```bash
export SECRET_KEY=your-secret-key-here
# On Windows: set SECRET_KEY=your-secret-key-here
```

5. **Run the application**
```bash
python app.py
```

6. **Open in browser**
Visit `http://localhost:5000`

### Database Initialization
The database is automatically created when you first run the application. Default categories are added for new users.

## 🌐 Deployment to Render

### Automatic Deployment

1. **Fork this repository** to your GitHub account

2. **Connect to Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure deployment**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment Variables:**
     - `SECRET_KEY`: Generate a secure random key

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app

### Manual Deployment

Alternatively, use the included `render.yaml` for infrastructure-as-code deployment.

## 📖 Usage Guide

### Getting Started
1. **Register** a new account or log in
2. **Add categories** for your spending (or use defaults)
3. **Record transactions** - both income and expenses
4. **View dashboard** for financial overview
5. **Analyze reports** to understand spending patterns

### Best Practices
- **Record transactions promptly** for accuracy
- **Use descriptive names** for easy identification
- **Categorize consistently** for better analytics
- **Review reports monthly** to track progress
- **Export data regularly** for backup

### Tips for Financial Management
- Set monthly budgets for each category
- Aim for a 20% savings rate
- Track both fixed and variable expenses
- Review spending patterns weekly
- Use the analytics to identify areas for improvement

## 🧪 Testing

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Adding different types of transactions
- [ ] Category management
- [ ] Dashboard data accuracy
- [ ] Chart visualization
- [ ] CSV export functionality
- [ ] Responsive design on mobile
- [ ] Error handling (404, 500 pages)

### Sample Data
Create test transactions to see the app in action:
- Income: Salary, Freelance, Investment returns
- Expenses: Groceries, Gas, Entertainment, Bills

## 🔒 Security Features

- **Password Hashing** - Using Werkzeug's secure hash algorithms
- **Session Management** - Secure user sessions with Flask
- **Input Validation** - Client and server-side validation
- **SQL Injection Prevention** - Parameterized queries
- **CSRF Protection** - Built-in Flask security measures

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute
1. **Report bugs** - Open an issue with detailed description
2. **Suggest features** - Share ideas for improvements
3. **Submit pull requests** - Fix bugs or add features
4. **Improve documentation** - Help others understand the project
5. **Share feedback** - Tell us about your experience

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 Changelog

### Version 1.0.0 (Current)
- ✅ User authentication system
- ✅ Transaction management
- ✅ Category system
- ✅ Dashboard with charts
- ✅ Reports and analytics
- ✅ CSV export
- ✅ Responsive design
- ✅ Error handling

### Planned Features (v1.1.0)
- 🔄 Budget tracking and alerts
- 🔄 Transaction editing and deletion
- 🔄 Multiple account support
- 🔄 Recurring transaction templates
- 🔄 Advanced filtering options
- 🔄 Email notifications
- 🔄 Dark mode theme

## 🐛 Known Issues

- Edit/Delete transaction functionality is placeholder (coming in v1.1.0)
- Budget management is database-ready but UI pending
- Charts use sample data on reports page (will connect to real data)

## 💡 Learning Outcomes

Building this project teaches:

### Technical Skills
- **Full-stack web development** with Python and JavaScript
- **Database design** and relationships
- **User authentication** and security
- **Data visualization** with Chart.js
- **Responsive web design** with Bootstrap
- **Cloud deployment** on Render
- **Version control** with Git

### Software Engineering
- **Project architecture** and file organization
- **API design** and RESTful endpoints
- **Error handling** and user experience
- **Code documentation** and best practices
- **Testing strategies** and quality assurance

### Financial Technology
- **Personal finance** application design
- **Data analytics** and visualization
- **User experience** in fintech apps
- **Financial calculations** and reporting

## 📞 Support

**Questions or issues?**
- 📧 Email: [your-email@example.com](mailto:your-email@example.com)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/personal-finance-tracker/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/personal-finance-tracker/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask** - Amazing web framework
- **Bootstrap** - Beautiful responsive design
- **Chart.js** - Powerful data visualization
- **Render** - Seamless deployment platform
- **Font Awesome** - Comprehensive icon library

---

**Built with ❤️ by [TheGhostPacket](https://github.com/TheGhostPacket)**

*Personal Finance Tracker - Take control of your financial future*