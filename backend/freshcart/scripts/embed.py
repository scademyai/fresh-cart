import click
from sqlalchemy import select

from freshcart.app import create_app
from freshcart.lib.embedder import embed_product
from freshcart.lib.models import db
from freshcart.lib.models.products import Product

app = create_app()


@click.command()
@click.option(
    "-p",
    "--product-id",
    type=int,
    default=None,
    help="Product id to embed",
)
@click.option(
    "-a",
    "--all",
    is_flag=True,
    default=False,
    help="Embed all non-embedded products",
)
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    help="Don't actually embed products",
)
@click.option(
    "-f",
    "--first",
    is_flag=True,
    default=False,
    help="Embed only the first product",
)
@click.pass_context
def main(ctx, product_id, all, dry_run, first):
    if product_id is None and not all and not first:
        click.echo("Must specify product id or --all or --first")
        return ctx.exit(1)

    with app.app_context():
        non_embedded_products = (
            [__get_first_product_id()]
            if first
            else __get_non_embedded_product_ids()
            if all
            else [product_id]
        )
        __embed_products(non_embedded_products, dry_run)


def __get_first_product_id():
    return db.session.scalars(
        select(Product.id).order_by(Product.id).limit(1)
    ).first()


def __get_non_embedded_product_ids():
    return db.session.scalars(
        select(Product.id).filter(Product.embedding == None)
    ).all()


def __embed_products(product_ids, dry_run):
    product_count = len(product_ids)
    embed_product_count = 0
    for product_id in product_ids:
        if not dry_run:
            click.echo(
                f"embed_product({product_id}) --- {embed_product_count/product_count*100:.2f}%"
            )
            embed_product(product_id)
        else:
            click.echo(f"dry_run: embed_product({product_id})")
        embed_product_count += 1

    click.echo(f"Embeddeding done - 100%")


if __name__ == "__main__":
    main()
