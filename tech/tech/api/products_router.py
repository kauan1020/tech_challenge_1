from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from tech.infra.databases.database import get_session
from tech.interfaces.gateways.product_gateway import ProductGateway
from tech.interfaces.schemas.product_schema import ProductSchema
from tech.use_cases.products.create_product_use_case import CreateProductUseCase
from tech.use_cases.products.list_products_by_category_use_case import ListProductsByCategoryUseCase
from tech.use_cases.products.list_all_products_use_case import ListAllProductsUseCase
from tech.use_cases.products.update_product_use_case import UpdateProductUseCase
from tech.use_cases.products.delete_product_use_case import DeleteProductUseCase
from tech.interfaces.controllers.product_controller import ProductController

router = APIRouter()

def get_product_controller(session: Session = Depends(get_session)) -> ProductController:
    """
    Dependency injection for the ProductController.

    This function initializes the controller by injecting the necessary use cases
    and the ProductGateway, ensuring proper separation of concerns.

    Args:
        session (Session): SQLAlchemy database session.

    Returns:
        ProductController: Instance of ProductController with required dependencies.
    """
    product_gateway = ProductGateway(session)
    return ProductController(
        create_product_use_case=CreateProductUseCase(product_gateway),
        list_products_by_category_use_case=ListProductsByCategoryUseCase(product_gateway),
        list_all_products_use_case=ListAllProductsUseCase(product_gateway),
        update_product_use_case=UpdateProductUseCase(product_gateway),
        delete_product_use_case=DeleteProductUseCase(product_gateway),
    )

@router.post('/', status_code=201)
def create_product(
    product: ProductSchema,
    controller: ProductController = Depends(get_product_controller)
) -> dict:
    """
    Creates a new product.

    Args:
        product (ProductSchema): The product details to be created.
        controller (ProductController): The ProductController instance.

    Returns:
        dict: The formatted response containing product details.
    """
    return controller.create_product(product)

@router.get('/{category}')
def list_products_by_category(
    category: str,
    controller: ProductController = Depends(get_product_controller)
) -> list:
    """
    Retrieves a list of products filtered by category.

    Args:
        category (str): The category to filter products by.
        controller (ProductController): The ProductController instance.

    Returns:
        list: A list of formatted product details.

    Raises:
        HTTPException: If no products are found in the specified category.
    """
    return controller.list_products_by_category(category)

@router.get('/')
def list_all_products(
    controller: ProductController = Depends(get_product_controller)
) -> list:
    """
    Retrieves all available products.

    Args:
        controller (ProductController): The ProductController instance.

    Returns:
        list: A list of formatted product details.

    Raises:
        HTTPException: If no products are found.
    """
    return controller.list_all_products()

@router.put('/{product_id}')
def update_product(
    product_id: int,
    product: ProductSchema,
    controller: ProductController = Depends(get_product_controller)
) -> dict:
    """
    Updates a product by its ID.

    Args:
        product_id (int): The ID of the product to update.
        product (ProductSchema): The updated product details.
        controller (ProductController): The ProductController instance.

    Returns:
        dict: The formatted response containing the updated product details.

    Raises:
        HTTPException: If the product is not found.
    """
    return controller.update_product(product_id, product)

@router.delete('/{product_id}')
def delete_product(
    product_id: int,
    controller: ProductController = Depends(get_product_controller)
) -> dict:
    """
    Deletes a product by its ID.

    Args:
        product_id (int): The ID of the product to delete.
        controller (ProductController): The ProductController instance.

    Returns:
        dict: A success message confirming deletion.

    Raises:
        HTTPException: If the product is not found.
    """
    return controller.delete_product(product_id)
