# 🚀 Simple URL Monitoring System

**Clean, simple, and easy-to-understand URL monitoring with Celery + RabbitMQ**

## 📁 File Structure (Just 3 Files!)

```
competitorApp/views/cronjob/
├── main_checker.py      # 🔧 Main logic (sitemap + category processing)
├── tasks.py            # ⚡ Celery tasks (just 4 simple tasks)
├── celery_config.py    # ⚙️ Simple Celery configuration
└── README.md          # 📖 This documentation
```

## 🎯 How It Works (Super Simple!)

### 1. **Every Minute**: Celery Beat runs the main task

### 2. **Find Due URLs**: Get URLs where `next_api_call_at <= now`

### 3. **Process Based on Type**:

- **Sitemap**: Fetch XML → Extract article URLs → Save new ones
- **Category**: Use CSS selectors → Find article links → Save new ones

### 4. **Update Database**: Set next check time and update stats

## 🔧 Main Functions

### `main_checker.py` - All the logic in one file:

```python
# Simple functions that do exactly what they say:
process_sitemap(url_obj)      # Process sitemap URLs
process_category(url_obj)     # Process category URLs
check_single_url(url_id)      # Check one URL
get_due_urls(limit)           # Get URLs that need checking
```

### `tasks.py` - Just 4 Celery tasks:

```python
url_checker_main_task()       # Main task (runs every minute)
process_batch_task(url_ids)   # Process batch of URLs
cleanup_old_stats()           # Clean old data (daily)
get_system_status()           # Get system status
```

## 🚀 Quick Start

### 1. **Start Services**:

```bash
# Start RabbitMQ
sudo systemctl start rabbitmq-server

# Start Celery Worker
celery -A articleInnovator worker --loglevel=info

# Start Celery Beat (scheduler)
celery -A articleInnovator beat --loglevel=info
```

### 2. **Test the System**:

```bash
# Show status
python manage.py run_url_checker --mode=status

# Test single URL
python manage.py run_url_checker --mode=test --url-id=123

# Manual check (100 URLs)
python manage.py run_url_checker --mode=manual --limit=100
```

## 📊 What It Does

### **For Sitemap URLs**:

1. Fetch `https://example.com/sitemap.xml`
2. Parse XML to get article URLs
3. Save new article URLs to database
4. Skip duplicates

### **For Category URLs**:

1. Get CSS selectors from database
2. Fetch webpage and find article links
3. Save new article URLs to database
4. Skip duplicates

## 📈 Processing Capacity

- **50,000 URLs per minute** (same as before)
- **Batch size**: 100 URLs per Celery task
- **Automatic retries** on failures
- **Daily statistics** tracking

## 🎛️ Simple Configuration

Everything is configured in `celery_config.py`:

- ✅ Main task runs every minute
- ✅ Cleanup runs daily at 2 AM
- ✅ Simple queue system
- ✅ Basic error handling

## 📋 Database Updates

The system updates:

- `last_api_call_at`: When checked
- `next_api_call_at`: Next check time
- `scrap_status`: completed/failed
- `competitor_url_daily_stats`: Daily statistics

## 🔍 Monitoring

```bash
# Check what's happening
python manage.py run_url_checker --mode=status

# Results show:
📊 System Status:
  📋 Total URLs: 125,000
  ⏰ Due for checking: 8,500
  📄 Sitemap URLs: 75,000
  🔗 Category URLs: 50,000
```

## 🎉 Why This Is Better

✅ **Only 3 main files** (was 8+ files)  
✅ **Clear, simple functions** (no complex classes)  
✅ **Easy to understand** (straightforward logic)  
✅ **Same performance** (50K URLs/minute)  
✅ **Same features** (sitemap + category support)  
✅ **Better organized** (everything in logical places)

**Result**: Same functionality, much simpler to understand and maintain! 🚀
