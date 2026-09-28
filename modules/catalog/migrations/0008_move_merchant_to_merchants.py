from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0007_alter_sellingcase_default_price"),
        ("merchants", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AlterField(
                    model_name="merchantproductconfiguration",
                    name="merchant",
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_configurations",
                        to="merchants.merchant",
                    ),
                ),
                migrations.DeleteModel(
                    name="Merchant",
                ),
            ],
        ),
    ]