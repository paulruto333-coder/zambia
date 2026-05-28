# momo Loan Application System

A complete Django-based loan application system with momo integration. Users can apply for loans with a multi-step process including applicant information, employment details, loan specifications, and momo verification.

## Features

- **Loan Application Form**: Comprehensive form collecting applicant information, employment details, and loan specifications
- **Dummy PIN/OTP Verification**: PIN and OTP fields accept any input and are saved to the database
- **Multi-Step Flow**:
  1. Loan Application Form (Step 1)
  2. momo Number + PIN Entry (Step 2)
  3. OTP Verification (Step 3)
  4. Success Confirmation
- **Records Page**: View all submitted loan applications with status tracking
- **Database Storage**: All applications and verification data saved to database
- **Admin Panel**: Django admin interface for managing applications

## Project Structure

```
momo_complete/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment configuration template
├── README.md                          # This file
├── momo_project_final/                   # Django project settings
│   ├── __init__.py
│   ├── settings.py                    # Project settings
│   ├── urls.py                        # URL routing
│   ├── wsgi.py                        # WSGI configuration
│   └── asgi.py                        # ASGI configuration
├── withdraw/                          # Django app
│   ├── migrations/                    # Database migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── templates/                     # HTML templates
│   │   ├── base.html                  # Base template
│   │   ├── landing.html               # Loan application form
│   │   ├── withdraw.html              # momo + PIN entry
│   │   ├── otp_verify.html            # OTP verification
│   │   ├── success.html               # Success confirmation
│   │   └── records.html               # All applications
│   ├── __init__.py
│   ├── admin.py                       # Django admin configuration
│   ├── models.py                      # LoanApplication model
│   ├── views.py                       # Application views
│   └── urls.py                        # App URL routing
└── frontend/
    └── static/
        └── images/                    # Static images (momo logo, etc.)
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone/Extract the Project
```bash
cd momo_complete
```

### Step 2: Create Virtual Environment
```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings (optional for development)
nano .env
```

### Step 5: Run Database Migrations
```bash
python manage.py migrate
```

### Step 6: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
# Follow the prompts to create an admin account
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## Usage

### For Users
1. **Visit the Application**: Go to `http://localhost:8000/`
2. **Fill Loan Application Form**: Enter all required information
3. **Enter momo Details**: Provide momo number and 4-digit PIN (dummy - accepts any input)
4. **Verify OTP**: Enter 6-digit OTP (dummy - accepts any input)
5. **View Success**: Confirmation page with application ID
6. **Check Records**: View all applications at `/records/`

### For Administrators
1. **Access Admin Panel**: Go to `http://localhost:8000/admin/`
2. **Login**: Use the superuser credentials created during setup
3. **Manage Applications**: View, filter, and edit loan applications
4. **View Details**: Click on any application to see full details

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET/POST | Loan application form |
| `/momo-entry/<id>/` | GET/POST | momo number and PIN entry |
| `/otp-verification/<id>/` | GET/POST | OTP verification |
| `/success/<id>/` | GET | Success confirmation |
| `/records/` | GET | View all applications |
| `/admin/` | GET | Django admin panel |

## Database Models

### LoanApplication
Stores all loan application data:

**Applicant Information**
- `full_name`: Applicant's full name
- `phone_number`: Contact phone number
- `email`: Email address
- `id_number`: ID or passport number
- `date_of_birth`: Date of birth
- `address`: Residential address

**Employment & Income**
- `professional_situation`: Employment status (employed, self-employed, etc.)
- `monthly_income`: Monthly income amount

**Loan Details**
- `loan_type`: Type of loan (personal, business, education, emergency)
- `loan_amount`: Requested loan amount
- `reimbursement_period`: Repayment period in months

**momo Verification**
- `momo_number`: momo phone number
- `pin`: 4-digit PIN (dummy field)
- `otp`: 6-digit OTP (dummy field)
- `pin_verified`: PIN verification status
- `otp_verified`: OTP verification status

**Status & Timestamps**
- `status`: Application status (pending, momo_entry, pin_verified, otp_verified, completed, failed)
- `created_at`: Application submission time
- `updated_at`: Last update time
- `momo_entered_at`: momo entry time
- `pin_verified_at`: PIN verification time
- `otp_verified_at`: OTP verification time
- `completed_at`: Completion time

## Key Features

### Dummy PIN/OTP System
- PIN and OTP fields accept any input
- No validation against real momo credentials
- All inputs are saved to the database for records
- Useful for testing and demonstration

### Multi-Step Form
- Progress tracking through application steps
- Form data persistence between steps
- Automatic redirects between steps
- Client-side validation

### Records Management
- View all submitted applications
- Filter by status or date
- Search by applicant name or phone
- Export application data (via admin panel)

## Configuration

### Database
By default, the project uses SQLite. To use PostgreSQL or MySQL:

1. Update `DATABASES` in `momo_project_final/settings.py`
2. Install the appropriate database driver
3. Run migrations

### Static Files
Static files (CSS, JavaScript, images) are served from `frontend/static/`. In production, run:
```bash
python manage.py collectstatic
```

### Email Notifications (Optional)
To enable email notifications, configure email settings in `momo_project_final/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-email-host'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email'
EMAIL_HOST_PASSWORD = 'your-password'
```

## Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn momo_project_final.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker
Create a `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "momo_project_final.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Using Railway/Render
1. Push code to GitHub
2. Connect repository to Railway/Render
3. Set environment variables
4. Deploy

## Important Notes

- **Dummy Verification**: PIN and OTP are not validated against real momo systems
- **Data Storage**: All application data is stored in the database
- **Security**: Implement proper authentication and authorization in production
- **Minimum Balance**: Users should have at least 10% of loan amount in momo account
- **Secret Key**: Change `SECRET_KEY` in production

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Errors
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

## Future Enhancements

- Real momo API integration
- Email notifications for application status
- SMS notifications via Twilio
- Admin approval workflow
- Loan disbursement tracking
- Application analytics dashboard
- Payment gateway integration
- User authentication system

## Support

For issues or questions, contact the development team.

## License

MIT License

## Version

1.0.0 - Initial Release
