**General**

User Activity Webhooks

* New user registration `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/user-registration\", \"body\": {\"event_type\": \"new_user_registered\", \"user_id\": \"u123456\", \"email\": \"newuser@example.com\", \"username\": \"newuser123\", \"registration_date\": \"2024-09-03T10:15:30Z\", \"source\": \"web_signup\", \"referral_code\": \"REF789\"}}"`
* User login/logout `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/user-auth\", \"body\": {\"event_type\": \"user_login\", \"user_id\": \"u789012\", \"username\": \"existinguser\", \"timestamp\": \"2024-09-03T11:30:45Z\", \"ip_address\": \"192.168.1.100\", \"device_type\": \"mobile\", \"login_method\": \"2fa\"}}"`
* Profile updates `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/profile-update\", \"body\": {\"event_type\": \"profile_updated\", \"user_id\": \"u345678\", \"updated_fields\": [\"name\", \"bio\", \"profile_picture\"], \"timestamp\": \"2024-09-03T14:20:00Z\", \"new_values\": {\"name\": \"Jane Smith\", \"bio\": \"Tech enthusiast and coffee lover\", \"profile_picture_url\": \"https://example.com/profiles/janesmith.jpg\"}}}"`
* Subscription changes `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/subscription-change\", \"body\": {\"event_type\": \"subscription_upgraded\", \"user_id\": \"u901234\", \"old_plan\": \"basic\", \"new_plan\": \"premium\", \"change_date\": \"2024-09-03T16:45:30Z\", \"next_billing_date\": \"2024-10-03T00:00:00Z\", \"payment_method\": \"credit_card\"}}"`

Content-Related Webhooks

* New content published `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/new-content\", \"body\": {\"event_type\": \"content_published\", \"content_id\": \"article_12345\", \"title\": \"10 Tips for Productive Remote Work\", \"author_id\": \"u567890\", \"publication_date\": \"2024-09-04T09:00:00Z\", \"category\": \"Productivity\", \"tags\": [\"remote work\", \"productivity\", \"tips\"], \"url\": \"https://example.com/blog/10-tips-productive-remote-work\"}}"`
* Content updates `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/content-update\", \"body\": {\"event_type\": \"content_updated\", \"content_id\": \"article_67890\", \"title\": \"Updated: Best Practices for Cloud Security\", \"author_id\": \"u123456\", \"update_date\": \"2024-09-04T11:30:00Z\", \"changes\": [\"title\", \"body\", \"tags\"], \"revision_number\": 3, \"url\": \"https://example.com/blog/best-practices-cloud-security\"}}"`
* Comments or reactions `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/user-interaction\", \"body\": {\"event_type\": \"new_comment\", \"content_id\": \"video_54321\", \"user_id\": \"u789012\", \"comment_id\": \"c98765\", \"comment_text\": \"Great video! Very informative.\", \"timestamp\": \"2024-09-04T14:15:30Z\", \"likes\": 5, \"replies\": 2}}"`

E-commerce Webhooks

* New order placed `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/new-order\", \"body\": {\"event_type\": \"order_placed\", \"order_id\": \"order_987654\", \"customer_id\": \"cust_12345\", \"order_date\": \"2024-09-05T10:00:00Z\", \"total_amount\": 129.99, \"currency\": \"USD\", \"items\": [{\"product_id\": \"prod_111\", \"quantity\": 2, \"price\": 59.99}, {\"product_id\": \"prod_222\", \"quantity\": 1, \"price\": 10.01}], \"shipping_address\": {\"street\": \"123 Main St\", \"city\": \"Anytown\", \"state\": \"CA\", \"zip\": \"12345\", \"country\": \"USA\"}}}"`
* Order status changes `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/order-status\", \"body\": {\"event_type\": \"order_status_changed\", \"order_id\": \"order_456789\", \"customer_id\": \"cust_67890\", \"old_status\": \"processing\", \"new_status\": \"shipped\", \"update_date\": \"2024-09-05T14:30:00Z\", \"tracking_number\": \"1Z999AA1234567890\", \"estimated_delivery_date\": \"2024-09-08T00:00:00Z\"}}"`
* Product inventory updates `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/inventory-update\", \"body\": {\"event_type\": \"inventory_changed\", \"product_id\": \"prod_333\", \"sku\": \"SKU123456\", \"old_quantity\": 100, \"new_quantity\": 75, \"update_date\": \"2024-09-05T16:45:00Z\", \"warehouse_id\": \"wh_001\", \"reorder_point\": 50, \"reorder_quantity\": 100}}"`
* Price changes `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/price-change\", \"body\": {\"event_type\": \"price_updated\", \"product_id\": \"prod_444\", \"sku\": \"SKU789012\", \"old_price\": 49.99, \"new_price\": 44.99, \"currency\": \"USD\", \"update_date\": \"2024-09-05T18:00:00Z\", \"reason\": \"seasonal_discount\", \"sale_start_date\": \"2024-09-06T00:00:00Z\", \"sale_end_date\": \"2024-09-20T23:59:59Z\"}}"`

IoT Device Data

* Sensor readings (temperature, humidity, motion, etc.) `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/sensor-data\", \"body\": {\"event_type\": \"sensor_reading\", \"device_id\": \"iot_device_123\", \"timestamp\": \"2024-09-06T10:15:30Z\", \"readings\": {\"temperature\": 22.5, \"humidity\": 45.2, \"motion_detected\": true}, \"battery_level\": 85, \"signal_strength\": -62}}"`
* Device status changes `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/device-status\", \"body\": {\"event_type\": \"device_status_change\", \"device_id\": \"iot_device_456\", \"timestamp\": \"2024-09-06T14:30:00Z\", \"old_status\": \"online\", \"new_status\": \"offline\", \"last_seen\": \"2024-09-06T14:29:55Z\", \"reason\": \"power_failure\"}}"`

Financial Data

* Stock price changes `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/stock-update\", \"body\": {\"event_type\": \"stock_price_change\", \"symbol\": \"AAPL\", \"timestamp\": \"2024-09-06T15:45:30Z\", \"old_price\": 150.25, \"new_price\": 152.75, \"currency\": \"USD\", \"percent_change\": 1.66, \"volume\": 1000000}}"`
* Currency exchange rate updates `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/forex-update\", \"body\": {\"event_type\": \"exchange_rate_update\", \"base_currency\": \"USD\", \"target_currency\": \"EUR\", \"timestamp\": \"2024-09-06T16:00:00Z\", \"old_rate\": 0.8450, \"new_rate\": 0.8475, \"percent_change\": 0.30}}"`
* Account balance notifications `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/account-update\", \"body\": {\"event_type\": \"balance_change\", \"account_id\": \"acc_789012\", \"timestamp\": \"2024-09-06T17:30:45Z\", \"old_balance\": 5000.00, \"new_balance\": 4800.00, \"currency\": \"USD\", \"transaction_type\": \"withdrawal\", \"transaction_id\": \"txn_123456\"}}"`

Weather Data

* Severe weather alerts `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/severe-alert\", \"body\": {\"event_type\": \"severe_weather_alert\", \"alert_id\": \"alert_987654\", \"location\": {\"city\": \"Miami\", \"state\": \"FL\", \"country\": \"USA\"}, \"alert_type\": \"hurricane_warning\", \"severity\": \"high\", \"start_time\": \"2024-09-07T08:00:00Z\", \"end_time\": \"2024-09-09T20:00:00Z\", \"description\": \"Hurricane approaching. Prepare for strong winds and heavy rainfall.\"}}"`
* Daily forecast updates `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/daily-forecast\", \"body\": {\"event_type\": \"daily_forecast_update\", \"location\": {\"city\": \"New York\", \"state\": \"NY\", \"country\": \"USA\"}, \"forecast_date\": \"2024-09-07\", \"temperature\": {\"high\": 28, \"low\": 18}, \"conditions\": \"partly_cloudy\", \"precipitation_chance\": 20, \"wind_speed\": 10, \"humidity\": 65}}"`

Scheduled Reminders

* Task due dates `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/task-reminder\", \"body\": {\"event_type\": \"task_due_soon\", \"task_id\": \"task_123456\", \"user_id\": \"user_789012\", \"task_title\": \"Complete project proposal\", \"due_date\": \"2024-09-08T17:00:00Z\", \"reminder_time\": \"2024-09-07T09:00:00Z\", \"priority\": \"high\"}}"`
* Appointment notifications `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/appointment-reminder\", \"body\": {\"event_type\": \"appointment_reminder\", \"appointment_id\": \"appt_987654\", \"user_id\": \"user_345678\", \"title\": \"Dental Check-up\", \"start_time\": \"2024-09-08T14:30:00Z\", \"end_time\": \"2024-09-08T15:30:00Z\", \"location\": \"123 Health St, Anytown, USA\", \"reminder_time\": \"2024-09-08T13:30:00Z\"}}"`
* Regular check-ins `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/check-in-reminder\", \"body\": {\"event_type\": \"regular_check_in\", \"user_id\": \"user_567890\", \"check_in_type\": \"daily_mood\", \"scheduled_time\": \"2024-09-07T20:00:00Z\", \"streak\": 7, \"last_check_in\": \"2024-09-06T20:15:30Z\", \"reminder_message\": \"Don't forget to log your mood for today!\"}}"`

Periodic Reports

* Daily/weekly/monthly summaries `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/summary\", \"body\": {\"report_type\": \"weekly\", \"start_date\": \"2024-09-01\", \"end_date\": \"2024-09-07\", \"total_users\": 15000, \"new_signups\": 450, \"revenue\": 75000.50, \"top_product\": \"Premium Plan\"}}"`
* Performance metrics `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/performance\", \"body\": {\"timestamp\": \"2024-09-08T00:00:00Z\", \"period\": \"daily\", \"metrics\": {\"average_response_time\": 250, \"error_rate\": 0.02, \"cpu_usage\": 65.5, \"memory_usage\": 78.2, \"active_users\": 5000}}}"`

Chat Platform Integrations

* New messages in connected platforms (Slack, Discord, etc.) `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/new-message\", \"body\": {\"platform\": \"slack\", \"channel_id\": \"C0123456789\", \"user_id\": \"U9876543210\", \"message\": \"Hello team!\", \"timestamp\": \"2024-09-08T10:15:30Z\", \"attachments\": [{\"type\": \"image\", \"url\": \"https://example.com/image.jpg\"}]}}"`
* Mentions or direct messages `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/mention\", \"body\": {\"platform\": \"discord\", \"type\": \"mention\", \"channel_id\": \"123456789012345678\", \"user_id\": \"987654321098765432\", \"mentioned_user_id\": \"112233445566778899\", \"message\": \"Hey @JohnDoe, can you review this?\", \"timestamp\": \"2024-09-08T11:30:45Z\"}}"`

Social Media Activity

* New posts or tweets `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/new-post\", \"body\": {\"platform\": \"twitter\", \"user_id\": \"12345678\", \"username\": \"techcompany\", \"post_id\": \"1234567890\", \"content\": \"Excited to announce our new product launch!\", \"timestamp\": \"2024-09-08T14:00:00Z\", \"likes\": 0, \"retweets\": 0, \"media\": [{\"type\": \"image\", \"url\": \"https://example.com/product.jpg\"}]}}"`
* Mentions or tags `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/mention\", \"body\": {\"platform\": \"instagram\", \"mentioned_user_id\": \"87654321\", \"mentioned_username\": \"ourcompany\", \"mentioning_user_id\": \"12345678\", \"mentioning_username\": \"influencer\", \"post_id\": \"9876543210\", \"content\": \"Loving the new gadget from @ourcompany!\", \"timestamp\": \"2024-09-08T15:30:00Z\"}}"`
* Follower milestones `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/follower-milestone\", \"body\": {\"platform\": \"facebook\", \"page_id\": \"123456789\", \"page_name\": \"Tech Innovations Inc.\", \"milestone\": 100000, \"total_followers\": 100000, \"timestamp\": \"2024-09-08T18:00:00Z\"}}"`

Error Notifications

* Application crashes `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/crash\", \"body\": {\"app_name\": \"MyMobileApp\", \"version\": \"2.1.3\", \"platform\": \"iOS\", \"device_model\": \"iPhone 12\", \"os_version\": \"15.1\", \"crash_time\": \"2024-09-08T20:45:30Z\", \"stack_trace\": \"Error: Unexpected null at line 42...\", \"user_id\": \"user_789012\"}}"`
* API failures `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/api-failure\", \"body\": {\"service\": \"payment_gateway\", \"endpoint\": \"/api/v1/process-payment\", \"http_method\": \"POST\", \"status_code\": 500, \"error_message\": \"Internal Server Error\", \"timestamp\": \"2024-09-08T21:15:00Z\", \"request_id\": \"req_987654\", \"client_ip\": \"203.0.113.42\"}}"`
* Performance issues `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/performance-issue\", \"body\": {\"service\": \"database\", \"issue_type\": \"high_latency\", \"current_value\": 500, \"threshold\": 200, \"unit\": \"ms\", \"timestamp\": \"2024-09-08T22:30:00Z\", \"affected_queries\": [\"SELECT * FROM users WHERE...\"], \"suggested_action\": \"optimize_query\"}}"`

Security Alerts

* Unusual login attempts `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/unusual-login\", \"body\": {\"event_type\": \"unusual_login_attempt\", \"user_id\": \"user_12345\", \"timestamp\": \"2024-09-09T08:30:00Z\", \"ip_address\": \"192.168.1.10\", \"location\": \"New York, USA\", \"device\": \"laptop\"}}"`
* Password changes `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/password-change\", \"body\": {\"event_type\": \"password_change\", \"user_id\": \"user_12345\", \"timestamp\": \"2024-09-09T09:00:00Z\", \"ip_address\": \"192.168.1.20\", \"action\": \"success\"}}"`
* Data access notifications `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/data-access\", \"body\": {\"event_type\": \"data_access_notification\", \"user_id\": \"user_12345\", \"timestamp\": \"2024-09-09T10:15:00Z\", \"accessed_data\": \"customer_records\", \"action\": \"viewed\"}}"`

**Smart Home Integration**

Temperature Control

* Receive webhooks from smart thermostats to adjust home temperature based on user preferences or schedules. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/temperature-control\", \"body\": {\"event_type\": \"temperature_control\", \"device_id\": \"thermostat_001\", \"timestamp\": \"2024-09-09T11:30:00Z\", \"target_temperature\": 22, \"current_temperature\": 20, \"user_id\": \"user_12345\"}}"`
* Trigger heating or cooling systems when the user is detected approaching home. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/user-detection\", \"body\": {\"event_type\": \"user_approaching\", \"device_id\": \"motion_sensor_001\", \"timestamp\": \"2024-09-09T12:00:00Z\", \"detected_user_id\": \"user_12345\", \"action\": \"trigger_heating\"}}"`

Security Alerts

* Get notifications from smart doorbells or security cameras when motion is detected. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/motion-detection\", \"body\": {\"event_type\": \"motion_detected\", \"device_id\": \"doorbell_001\", \"timestamp\": \"2024-09-09T12:30:00Z\", \"location\": \"front_door\", \"action\": \"notify_owner\"}}"`
* Trigger home security system arming/disarming based on user location. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/security-system\", \"body\": {\"event_type\": \"security_system_status\", \"device_id\": \"security_panel_001\", \"timestamp\": \"2024-09-09T12:45:00Z\", \"location\": \"home\", \"action\": \"arm_system\", \"user_id\": \"user_12345\"}}"`

**Health and Fitness**

Fitness Tracking

* Receive webhooks from fitness devices to log daily activity, steps, or workouts. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/activity-log\", \"body\": {\"user_id\": \"user_135790\", \"device_id\": \"fitbit_789\", \"date\": \"2024-09-09\", \"steps\": 8500, \"calories_burned\": 2200, \"active_minutes\": 65, \"distance\": 6.8, \"distance_unit\": \"km\", \"heart_rate_avg\": 72}}"`
* Trigger reminders or suggestions based on activity levels. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/activity-suggestion\", \"body\": {\"user_id\": \"user_246810\", \"event_type\": \"low_activity_alert\", \"current_steps\": 2000, \"daily_goal\": 10000, \"current_time\": \"2024-09-09T16:30:00Z\", \"suggestion\": \"Take a 15-minute walk to boost your step count!\", \"weather\": {\"condition\": \"clear\", \"temperature\": 22}}}"`

Sleep Monitoring

* Get data from sleep tracking devices to analyze sleep patterns. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/sleep-data\", \"body\": {\"user_id\": \"user_123456\", \"timestamp\": \"2024-09-10T06:30:00Z\", \"sleep_pattern\": {\"duration\": 8, \"quality\": \"good\", \"stages\": {\"deep_sleep\": 120, \"light_sleep\": 300, \"rem_sleep\": 90}}, \"wakeup_time\": \"2024-09-10T07:00:00Z\"}}"`
* Adjust smart home settings (like lighting or temperature) based on sleep schedules. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/sleep-schedule\", \"body\": {\"user_id\": \"user_123456\", \"event_type\": \"adjust_settings\", \"timestamp\": \"2024-09-10T22:00:00Z\", \"preferred_temperature\": 20.0, \"light_intensity\": \"dim\"}}"`

**Productivity and Time Management**

Calendar Integration

* Receive webhooks for new calendar events or changes. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/new-event\", \"body\": {\"event_type\": \"new_calendar_event\", \"event_id\": \"event_789012\", \"user_id\": \"user_123456\", \"title\": \"Team Meeting\", \"start_time\": \"2024-09-11T09:00:00Z\", \"end_time\": \"2024-09-11T10:00:00Z\", \"location\": \"Conference Room A\"}}"`
* Trigger travel time calculations and reminders based on upcoming appointments. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/travel-time\", \"body\": {\"event_type\": \"travel_time_calculation\", \"user_id\": \"user_123456\", \"event_id\": \"event_789012\", \"departure_time\": \"2024-09-11T08:30:00Z\", \"origin\": \"123 Main St, City\", \"destination\": \"Conference Room A\", \"estimated_travel_time\": 15}}"`

  Task Management
* Get notifications when tasks are added, completed, or approaching deadlines in task management apps. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/task-approaching-deadline\", \"body\": {\"event_type\": \"task_due_soon\", \"task_id\": \"task_654321\", \"user_id\": \"user_123456\", \"title\": \"Prepare presentation\", \"due_date\": \"2024-09-15T16:00:00Z\", \"days_remaining\": 5}}"`
* Automatically create follow-up tasks based on completed items. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/task-update\", \"body\": {\"event_type\": \"task_completed\", \"task_id\": \"task_456789\", \"user_id\": \"user_123456\", \"title\": \"Submit report\", \"completed_time\": \"2024-09-10T11:00:00Z\", \"follow_up_task\": {\"title\": \"Review report\", \"due_date\": \"2024-09-12T17:00:00Z\"}}}"`

**Financial Management**

Bank Transactions

* Receive webhooks for new transactions or account balance changes. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/new-transaction\", \"body\": {\"event_type\": \"new_transaction\", \"transaction_id\": \"txn_123456\", \"user_id\": \"user_123456\", \"amount\": 250.75, \"currency\": \"USD\", \"transaction_date\": \"2024-09-09T12:30:00Z\", \"merchant\": \"Online Shop\", \"category\": \"Shopping\"}}"`
* Trigger budget alerts or savings recommendations based on spending patterns. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/budget-alert\", \"body\": {\"event_type\": \"budget_alert\", \"user_id\": \"user_123456\", \"category\": \"Dining\", \"spending_limit\": 200.00, \"current_spending\": 220.00, \"alert_time\": \"2024-09-09T14:30:00Z\"}}"`

  Bill Payments
* Get notifications for upcoming bills or successful payments. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/bill-reminder\", \"body\": {\"event_type\": \"upcoming_bill\", \"user_id\": \"user_123456\", \"bill_id\": \"bill_456789\", \"amount_due\": 75.50, \"due_date\": \"2024-09-15T00:00:00Z\", \"service\": \"Electricity\"}}"`
* Automatically categorize expenses for budgeting purposes. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/expense-categorization\", \"body\": {\"event_type\": \"expense_categorized\", \"user_id\": \"user_123456\", \"transaction_id\": \"txn_123456\", \"category\": \"Clothing\", \"amount\": 49.99, \"timestamp\": \"2024-09-09T13:00:00Z\"}}"`

**Travel and Commute**

Traffic Updates

* Receive webhooks with real-time traffic information. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/traffic-update\", \"body\": {\"event_type\": \"traffic_alert\", \"route_id\": \"route_123\", \"start_point\": \"123 Main St, City A\", \"end_point\": \"456 Oak Ave, City B\", \"current_travel_time\": 45, \"usual_travel_time\": 30, \"delay_reason\": \"accident\", \"timestamp\": \"2024-09-11T08:15:00Z\"}}"`
* Trigger alternative route suggestions or departure time adjustments. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/route-suggestion\", \"body\": {\"event_type\": \"alternative_route\", \"user_id\": \"user_789\", \"original_route_id\": \"route_123\", \"alternative_route_id\": \"route_456\", \"estimated_time_saved\": 15, \"departure_time_adjustment\": \"+20 minutes\", \"timestamp\": \"2024-09-11T08:20:00Z\"}}"`

  Public Transit
* Get notifications about delays or service changes on frequently used routes. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/service-update\", \"body\": {\"event_type\": \"transit_delay\", \"route_id\": \"bus_101\", \"delay_minutes\": 10, \"reason\": \"traffic congestion\", \"affected_stops\": [\"stop_A\", \"stop_B\", \"stop_C\"], \"estimated_resolution_time\": \"2024-09-11T09:30:00Z\", \"timestamp\": \"2024-09-11T08:45:00Z\"}}"`
* Trigger reminders to leave earlier if delays are detected. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/early-departure\", \"body\": {\"event_type\": \"early_departure_reminder\", \"user_id\": \"user_456\", \"usual_departure_time\": \"2024-09-11T08:30:00Z\", \"suggested_departure_time\": \"2024-09-11T08:15:00Z\", \"reason\": \"15-minute delay on bus route 101\", \"timestamp\": \"2024-09-11T07:45:00Z\"}}"`

**Weather-based Actions**

Severe Weather Alerts

* Receive webhooks for severe weather warnings. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/severe-weather\", \"body\": {\"event_type\": \"severe_weather_warning\", \"alert_type\": \"thunderstorm\", \"severity\": \"high\", \"location\": {\"city\": \"Springfield\", \"state\": \"IL\", \"country\": \"USA\"}, \"start_time\": \"2024-09-11T14:00:00Z\", \"end_time\": \"2024-09-11T18:00:00Z\", \"description\": \"Severe thunderstorm with potential for hail and strong winds\", \"timestamp\": \"2024-09-11T13:30:00Z\"}}"`
* Trigger smart home actions like closing windows or adjusting HVAC systems. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/weather-action\", \"body\": {\"event_type\": \"weather_based_action\", \"home_id\": \"home_123\", \"action\": \"close_windows\", \"reason\": \"incoming thunderstorm\", \"hvac_adjustment\": {\"mode\": \"cool\", \"temperature\": 22}, \"timestamp\": \"2024-09-11T13:35:00Z\"}}"`

  Daily Forecast
* Get daily weather forecasts and trigger clothing or activity suggestions. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/daily-forecast\", \"body\": {\"event_type\": \"daily_forecast\", \"user_id\": \"user_789\", \"location\": {\"city\": \"New York\", \"state\": \"NY\", \"country\": \"USA\"}, \"date\": \"2024-09-12\", \"forecast\": {\"high_temp\": 28, \"low_temp\": 18, \"condition\": \"partly cloudy\", \"precipitation_chance\": 20}, \"clothing_suggestion\": \"Light jacket recommended for morning chill\", \"activity_suggestion\": \"Great day for an afternoon picnic in the park\", \"timestamp\": \"2024-09-11T22:00:00Z\"}}"`

**Social Media and Communication**

Message Notifications

* Receive webhooks for new messages across various platforms. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/new-message\", \"body\": {\"event_type\": \"new_message\", \"platform\": \"slack\", \"user_id\": \"user_123\", \"channel_id\": \"C0123456789\", \"message_id\": \"msg_987654\", \"content\": \"Hello, how can I help you?\", \"timestamp\": \"2024-09-11T10:00:00Z\"}}"`
* Trigger priority notifications for important contacts. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/priority-notification\", \"body\": {\"event_type\": \"priority_notification\", \"user_id\": \"user_456\", \"contact_id\": \"contact_789\", \"message\": \"Urgent: Please check this out!\", \"timestamp\": \"2024-09-11T10:05:00Z\"}}"`

  Social Media Updates
* Get notifications for mentions or interactions on social media platforms. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/mention\", \"body\": {\"event_type\": \"mention\", \"platform\": \"twitter\", \"user_id\": \"user_321\", \"mentioning_user\": \"influencer_987\", \"content\": \"@user_321 Check this out!\", \"timestamp\": \"2024-09-11T10:10:00Z\"}}"`
* Trigger content suggestions or scheduling based on engagement patterns. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/content-suggestion\", \"body\": {\"event_type\": \"engagement_suggestion\", \"user_id\": \"user_321\", \"suggested_content\": \"Consider posting more about tech tips.\", \"engagement_metrics\": {\"likes\": 150, \"shares\": 50}, \"timestamp\": \"2024-09-11T10:15:00Z\"}}"`

**Shopping and Inventory Management**

Smart Fridge Integration

* Receive webhooks when food items are running low. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/low-inventory\", \"body\": {\"event_type\": \"low_inventory\", \"user_id\": \"user_123\", \"item_id\": \"item_456\", \"item_name\": \"Milk\", \"current_quantity\": 1, \"timestamp\": \"2024-09-11T11:00:00Z\"}}"`
* Trigger automatic additions to shopping lists or online grocery orders. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/add-to-shopping-list\", \"body\": {\"event_type\": \"add_to_shopping_list\", \"user_id\": \"user_123\", \"item_name\": \"Milk\", \"quantity\": 2, \"timestamp\": \"2024-09-11T11:05:00Z\"}}"`

  Package Tracking
* Get notifications for package shipments and deliveries. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/shipment-update\", \"body\": {\"event_type\": \"shipment_notification\", \"tracking_number\": \"TRACK123456\", \"carrier\": \"UPS\", \"status\": \"Out for delivery\", \"estimated_delivery_time\": \"2024-09-11T16:00:00Z\", \"timestamp\": \"2024-09-11T15:00:00Z\"}}"`
* Trigger reminders to be at home for important deliveries. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/delivery-reminder\", \"body\": {\"event_type\": \"reminder_notification\", \"user_id\": \"user_123\", \"tracking_number\": \"TRACK123456\", \"reminder_time\": \"2024-09-11T15:00:00Z\", \"message\": \"Your package will arrive soon. Please be available at home.\", \"timestamp\": \"2024-09-11T14:00:00Z\"}}"`

**Google Calendar**

Event Creation Webhook

* Trigger when a new event is created in a specific calendar. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/calendar/event-created\", \"body\": {\"event_type\": \"event_created\", \"calendar_id\": \"primary\", \"event_id\": \"abc123xyz\", \"summary\": \"Team Meeting\", \"start\": {\"dateTime\": \"2024-09-15T10:00:00Z\"}, \"end\": {\"dateTime\": \"2024-09-15T11:00:00Z\"}, \"creator\": {\"email\": \"organizer@example.com\"}, \"attendees\": [{\"email\": \"attendee1@example.com\"}, {\"email\": \"attendee2@example.com\"}]}}"`

Event Update Webhook

* Activate when an existing event is modified (time, date, or details changed). `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/calendar/event-updated\", \"body\": {\"event_type\": \"event_updated\", \"calendar_id\": \"primary\", \"event_id\": \"def456uvw\", \"summary\": \"Project Review\", \"changes\": {\"old_start\": {\"dateTime\": \"2024-09-16T14:00:00Z\"}, \"new_start\": {\"dateTime\": \"2024-09-16T15:00:00Z\"}, \"old_end\": {\"dateTime\": \"2024-09-16T15:00:00Z\"}, \"new_end\": {\"dateTime\": \"2024-09-16T16:00:00Z\"}}, \"organizer\": {\"email\": \"manager@example.com\"}}}"`

Attendee Response Webhook

* Fire when an attendee responds to an event invitation. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/calendar/attendee-response\", \"body\": {\"event_type\": \"attendee_response\", \"calendar_id\": \"primary\", \"event_id\": \"ghi789rst\", \"summary\": \"Quarterly Review\", \"attendee\": {\"email\": \"employee@example.com\"}, \"response_status\": \"accepted\", \"timestamp\": \"2024-09-17T09:30:00Z\"}}"`

**Google Chat**

Message Received Webhook

* Trigger when a new message is posted in a specific Chat space or room. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/v1/spaces/SPACE_ID/messages\", \"body\": {\"type\": \"MESSAGE\", \"eventTime\": \"2024-09-18T13:45:00Z\", \"message\": {\"name\": \"spaces/SPACE_ID/messages/MESSAGE_ID\", \"sender\": {\"name\": \"users/12345\", \"displayName\": \"John Doe\", \"email\": \"johndoe@example.com\"}, \"createTime\": \"2024-09-18T13:45:00Z\", \"text\": \"Hello team, any updates on the project?\", \"thread\": {\"name\": \"spaces/SPACE_ID/threads/THREAD_ID\"}}, \"space\": {\"name\": \"spaces/SPACE_ID\", \"type\": \"ROOM\"}}}"`

Bot Mention Webhook

* Activate when a Chat bot is mentioned in a conversation. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/v1/spaces/SPACE_ID/messages\", \"body\": {\"type\": \"MESSAGE\", \"eventTime\": \"2024-09-19T10:00:00Z\", \"message\": {\"name\": \"spaces/SPACE_ID/messages/MESSAGE_ID\", \"sender\": {\"name\": \"users/67890\", \"displayName\": \"Jane Smith\", \"email\": \"janesmith@example.com\"}, \"createTime\": \"2024-09-19T10:00:00Z\", \"text\": \"@MyBot what's the status of the server?\", \"annotations\": [{\"type\": \"USER_MENTION\", \"startIndex\": 0, \"length\": 6, \"userMention\": {\"user\": {\"name\": \"users/BOT_ID\", \"displayName\": \"MyBot\"}}}], \"thread\": {\"name\": \"spaces/SPACE_ID/threads/THREAD_ID\"}}, \"space\": {\"name\": \"spaces/SPACE_ID\", \"type\": \"ROOM\"}}}"`

File Share Webhook

* Fire when a file is shared in a Chat space. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/file-share\", \"body\": {\"event_type\": \"file_shared\", \"space_id\": \"space_123456\", \"user_id\": \"user_789012\", \"file_id\": \"file_345678\", \"file_name\": \"project_proposal.pdf\", \"file_size\": 2048576, \"share_time\": \"2024-09-12T10:00:00Z\"}}"`

**Gmail**

New Email Webhook

* Trigger when a new email is received in a specific Gmail account or label. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/new-email\", \"body\": {\"event_type\": \"new_email_received\", \"account_id\": \"user@example.com\", \"email_id\": \"email_123456\", \"subject\": \"Meeting Agenda\", \"sender\": \"colleague@company.com\", \"received_time\": \"2024-09-12T10:15:00Z\", \"label\": \"Work\"}}"`

Email Sent Webhook

* Activate when an email is sent from a Gmail account. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/email-sent\", \"body\": {\"event_type\": \"email_sent\", \"account_id\": \"user@example.com\", \"email_id\": \"email_789012\", \"subject\": \"Project Update\", \"recipient\": \"manager@company.com\", \"sent_time\": \"2024-09-12T10:30:00Z\"}}"`

**Google Sheets**

Row Added Webhook

* Trigger when a new row is added to a specific Google Sheet. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/row-added\", \"body\": {\"event_type\": \"row_added\", \"sheet_id\": \"sheet_123456\", \"sheet_name\": \"Sales Data\", \"row_number\": 42, \"added_by\": \"user@example.com\", \"timestamp\": \"2024-09-12T11:00:00Z\"}}"`

Cell Update Webhook

* Activate when a specific cell or range is updated in a Sheet. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/cell-update\", \"body\": {\"event_type\": \"cell_updated\", \"sheet_id\": \"sheet_789012\", \"sheet_name\": \"Budget\", \"cell_range\": \"B15:B20\", \"updated_by\": \"user@example.com\", \"old_value\": 1000, \"new_value\": 1500, \"timestamp\": \"2024-09-12T11:15:00Z\"}}"`

Form Response Webhook

* Fire when a new response is submitted to a Google Form linked to a Sheet. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/form-response\", \"body\": {\"event_type\": \"form_submitted\", \"form_id\": \"form_345678\", \"response_id\": \"response_901234\", \"submitted_by\": \"respondent@example.com\", \"submission_time\": \"2024-09-12T11:30:00Z\", \"linked_sheet_id\": \"sheet_567890\"}}"`

**Discord**

Message Reaction Webhook

* Trigger when a user reacts to a message in a specific channel. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/message-reaction\", \"body\": {\"event_type\": \"message_reaction\", \"server_id\": \"server_123456\", \"channel_id\": \"channel_789012\", \"message_id\": \"msg_345678\", \"user_id\": \"user_901234\", \"emoji\": \"👍\", \"reaction_time\": \"2024-09-12T12:00:00Z\"}}"`

User Join/Leave Webhook

* Activate when a user joins or leaves a server. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/user-membership\", \"body\": {\"event_type\": \"user_joined\", \"server_id\": \"server_567890\", \"user_id\": \"user_123456\", \"username\": \"NewUser#1234\", \"join_time\": \"2024-09-12T12:15:00Z\"}}"`

**Slack**

Slash Command Webhook

* Trigger when a user enters a custom slash command. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/slash-command\", \"body\": {\"event_type\": \"slash_command\", \"team_id\": \"T12345\", \"channel_id\": \"C67890\", \"user_id\": \"U13579\", \"command\": \"/todo\", \"text\": \"Add new task: Update documentation\", \"timestamp\": \"2024-09-12T12:30:00Z\"}}"`

Interactive Message Webhook

* Activate when a user interacts with buttons or menus in a Slack message. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/interactive-message\", \"body\": {\"event_type\": \"interactive_message\", \"team_id\": \"T12345\", \"channel_id\": \"C67890\", \"user_id\": \"U13579\", \"message_ts\": \"1631448600.000100\", \"action\": {\"type\": \"button\", \"name\": \"approve\", \"value\": \"yes\"}, \"timestamp\": \"2024-09-12T12:45:00Z\"}}"`

**WhatsApp**

Incoming Message Webhook

* Trigger when a new message is received from a customer. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/incoming-message\", \"body\": {\"event_type\": \"incoming_message\", \"message_id\": \"msg_123456\", \"from\": \"+1234567890\", \"to\": \"+0987654321\", \"content\": \"Hello, I have a question about my order.\", \"timestamp\": \"2024-09-12T10:00:00Z\", \"media_type\": \"text\"}}"`

Status Update Webhook

* Activate when a message status changes (sent, delivered, read). `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/status-update\", \"body\": {\"event_type\": \"message_status_update\", \"message_id\": \"msg_789012\", \"status\": \"read\", \"recipient\": \"+1234567890\", \"timestamp\": \"2024-09-12T10:05:00Z\"}}"`

**LinkedIn**

New Connection Webhook

* Trigger when a new connection is made. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/new-connection\", \"body\": {\"event_type\": \"new_connection\", \"user_id\": \"user_123456\", \"connection_id\": \"conn_789012\", \"connection_name\": \"Jane Doe\", \"connection_title\": \"Marketing Manager at Tech Co.\", \"timestamp\": \"2024-09-12T11:00:00Z\"}}"`

Post Engagement Webhook

* Activate when someone likes, comments, or shares a post. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/post-engagement\", \"body\": {\"event_type\": \"post_engagement\", \"post_id\": \"post_345678\", \"user_id\": \"user_123456\", \"engagement_type\": \"comment\", \"engaging_user_id\": \"user_987654\", \"engagement_content\": \"Great insights! Thanks for sharing.\", \"timestamp\": \"2024-09-12T11:30:00Z\"}}"`

**Twitter**

New Mention Webhook

* Trigger when the account is mentioned in a tweet. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/new-mention\", \"body\": {\"event_type\": \"new_mention\", \"tweet_id\": \"1234567890\", \"mentioned_user\": \"@YourCompany\", \"mentioning_user\": \"@Customer123\", \"tweet_text\": \"Hey @YourCompany, loving your new product!\", \"timestamp\": \"2024-09-12T12:00:00Z\"}}"`

New Follower Webhook

* Activate when a new user follows the account. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/new-follower\", \"body\": {\"event_type\": \"new_follower\", \"follower_id\": \"user_567890\", \"follower_username\": \"@NewFollower\", \"follower_name\": \"New Follower\", \"follower_bio\": \"Tech enthusiast and coffee lover\", \"timestamp\": \"2024-09-12T12:30:00Z\"}}"`

**Reddit**

New Post in Subreddit Webhook

* Trigger when a new post is made in a specific subreddit. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/new-subreddit-post\", \"body\": {\"event_type\": \"new_subreddit_post\", \"subreddit\": \"r/technology\", \"post_id\": \"abcdef\", \"title\": \"New AI breakthrough announced\", \"author\": \"u/techgeek\", \"url\": \"https://www.reddit.com/r/technology/comments/abcdef/new_ai_breakthrough_announced/\", \"timestamp\": \"2024-09-12T13:00:00Z\"}}"`

Comment by Specific User Webhook

* Activate when a specified user comments in a particular subreddit. `"{\"method\": \"POST\", \"url\": \"http://localhost:8000/webhook/user-comment\", \"body\": {\"event_type\": \"user_comment\", \"user\": \"u/specific_user\", \"subreddit\": \"r/AskScience\", \"comment_id\": \"comm_123456\", \"post_id\": \"post_789012\", \"comment_text\": \"This is fascinating! I wonder how it will impact future research.\", \"timestamp\": \"2024-09-12T13:30:00Z\"}}"`
