# Shopping Cart API Guide

## Overview
A fully functional shopping cart system with automatic inventory checking, duplicate prevention, and comprehensive cart management.

## Features
- ✅ Create and manage shopping carts with UUID identifiers
- ✅ Add/update/remove items from cart
- ✅ Automatic inventory validation
- ✅ Prevent duplicate products (auto-increment quantity)
- ✅ Calculate total price and item count
- ✅ Clear entire cart with one action
- ✅ Nested RESTful endpoints

## API Endpoints

### Cart Management

#### List All Carts
```
GET /store/carts/
```

#### Create a New Cart
```
POST /store/carts/
```
Response includes a UUID cart ID that you'll use for all cart operations.

#### Get Cart Details
```
GET /store/carts/{cart_id}/
```
Returns cart with all items, total price, and total item count.

#### Delete a Cart
```
DELETE /store/carts/{cart_id}/
```

#### Clear Cart Items
```
POST /store/carts/{cart_id}/clear/
```
Removes all items but keeps the cart.

---

### Cart Items Management

#### List Items in Cart
```
GET /store/carts/{cart_id}/items/
```

#### Add Item to Cart
```
POST /store/carts/{cart_id}/items/
Content-Type: application/json

{
    "product_id": 1,
    "quantity": 2
}
```

**Smart Logic:**
- If product already exists in cart, quantity is added to existing quantity
- Validates inventory availability
- Returns error if insufficient stock

#### Get Single Cart Item
```
GET /store/carts/{cart_id}/items/{item_id}/
```

#### Update Item Quantity
```
PATCH /store/carts/{cart_id}/items/{item_id}/
Content-Type: application/json

{
    "quantity": 5
}
```
Validates inventory before updating.

#### Remove Item from Cart
```
DELETE /store/carts/{cart_id}/items/{item_id}/
```

---

## Usage Examples

### Example 1: Creating a Shopping Cart

```bash
# 1. Create a cart
curl -X POST http://localhost:8000/store/carts/

# Response:
{
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "created_at": "2026-02-16T18:30:00Z",
    "items": [],
    "total_price": "0.00",
    "total_items": 0
}
```

### Example 2: Adding Items to Cart

```bash
# Add first product
curl -X POST http://localhost:8000/store/carts/a1b2c3d4.../items/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'

# Response:
{
    "id": 1,
    "product": {
        "id": 1,
        "title": "Product Name",
        "unit_price": "25.99"
    },
    "product_id": 1,
    "quantity": 2,
    "total_price": "51.98"
}

# Add same product again (quantity will be added)
curl -X POST http://localhost:8000/store/carts/a1b2c3d4.../items/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 1}'

# Now the cart item will have quantity: 3
```

### Example 3: Viewing Cart

```bash
curl http://localhost:8000/store/carts/a1b2c3d4.../

# Response:
{
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "created_at": "2026-02-16T18:30:00Z",
    "items": [
        {
            "id": 1,
            "product": {
                "id": 1,
                "title": "Product Name",
                "unit_price": "25.99"
            },
            "product_id": 1,
            "quantity": 3,
            "total_price": "77.97"
        }
    ],
    "total_price": "77.97",
    "total_items": 3
}
```

### Example 4: Updating Quantity

```bash
curl -X PATCH http://localhost:8000/store/carts/a1b2c3d4.../items/1/ \
  -H "Content-Type: application/json" \
  -d '{"quantity": 5}'
```

### Example 5: Removing Items

```bash
# Remove specific item
curl -X DELETE http://localhost:8000/store/carts/a1b2c3d4.../items/1/

# Or clear entire cart
curl -X POST http://localhost:8000/store/carts/a1b2c3d4.../clear/
```

---

## Validation & Business Logic

### Inventory Validation
- ✅ Checks if product has sufficient inventory before adding/updating
- ✅ Returns error: "Insufficient inventory" if stock is too low

### Duplicate Prevention
- ✅ If you add a product already in cart, it updates the quantity instead of creating duplicate
- ✅ Enforced by database unique_together constraint on (cart, product)

### Data Integrity
- ✅ Product must exist (validated before creation)
- ✅ Quantity must be at least 1
- ✅ Cart items cascade delete when cart is deleted
- ✅ UUID prevents cart ID collisions

---

## Models Structure

### Cart
- `id`: UUID (primary key)
- `created_at`: DateTime

### CartItem
- `id`: Integer (primary key)
- `cart`: ForeignKey to Cart
- `product`: ForeignKey to Product
- `quantity`: PositiveSmallInteger
- Unique constraint: (cart, product)

---

## Testing the Cart

You can test the cart system using:
- **cURL** (see examples above)
- **Postman/Insomnia** - Import the endpoints
- **Django REST Framework browsable API** - Navigate to http://localhost:8000/store/carts/
- **Python requests library**

---

## Notes

1. **UUID Cart IDs**: Each cart gets a unique UUID, perfect for guest checkout or temporary carts
2. **Performance**: Uses `select_related` and `prefetch_related` for optimized queries
3. **RESTful**: Follows REST conventions with nested routes
4. **Validation**: All operations validate inventory and data integrity
5. **Idempotent**: Safe to retry operations without side effects
