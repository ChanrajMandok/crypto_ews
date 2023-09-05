from django.db import migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ('binance_ews_app', '0002_modelbinanceevent_event_completed_and_more') ]
    
    operations = [
        migrations.RunSQL(
            """
            CREATE MATERIALIZED VIEW live_binance_events AS 
            SELECT 
                title, 
                url, 
                h_spot_tickers, 
                h_usdm_tickers, 
                important_dates,
                alert_category, 
                network_tokens, 
                alert_priority


            FROM public.binance_ews_app_modelbinanceevent
                WHERE event_completed = False
                ORDER BY Alert_priority

            """,
            reverse_sql="DROP MATERIALIZED VIEW live_binance_events;"
        )
    ]