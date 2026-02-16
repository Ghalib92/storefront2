# Cart Data Population Summary

## ✅ Successfully Created

### Database Contents:
- **10 Shopping Carts** with realistic data
- **52 Cart Items** distributed across carts
- **Total Value**: Over $40,000 in simulated orders

### Cart Distribution:
```
Cart 1:  7 products, 23 items → $3,584.77
Cart 2:  7 products, 21 items → $4,563.79
Cart 3:  7 products, 22 items → $1,277.78
Cart 4:  1 product,   5 items → $6,499.95
Cart 5:  8 products, 22 items → $7,295.78
Cart 6:  4 products, 16 items → $7,409.84
Cart 7:  7 products, 28 items → $3,824.72
Cart 8:  7 products, 20 items → $2,251.80
Cart 9:  3 products,  6 items → $199.94
Cart 10: 1 product,   5 items → $6,499.95
```

## 🔧 Management Commands

### Seed Carts
```bash
python manage.py seed_carts --carts 10
```
Creates shopping carts with random products and quantities.

**Options:**
- `--carts N` - Number of carts to create (default: 5)

**Features:**
- ✅ Clears existing carts before creating new ones
- ✅ Validates product inventory
- ✅ Random selection of 1-8 products per cart
- ✅ Random quantities (1-5 items, based on stock)
- ✅ Shows summary with totals

### Other Available Commands
```bash
python manage.py seed_products  # Seed products first
python manage.py seed_reviews   # Add reviews to products
```

## 🌐 Testing the API

### Start the Server
```bash
python manage.py runserver
```

### Example API Calls

#### 1. List All Carts
```bash
curl http://localhost:8000/store/carts/
```

#### 2. Get Specific Cart with Items
```bash
curl http://localhost:8000/store/carts/17eed084-22f5-4334-ae9f-967e9df37abb/
```

**Response Example:**
```json
{
    "id": "17eed084-22f5-4334-ae9f-967e9df37abb",
    "created_at": "2026-02-16T17:55:22.561964Z",
    "items": [
        {
            "id": 1,
            "product": {
                "id": 2,
                "title": "Wireless Mouse",
                "unit_price": "29.99"
            },
            "quantity": 4,
            "total_price": "119.96"
        }
    ],
    "total_price": "199.94",
    "total_items": 6
}
```

#### 3. List Cart Items
```bash
curl http://localhost:8000/store/carts/17eed084-22f5-4334-ae9f-967e9df37abb/items/
```

#### 4. Add New Item to Cart
```bash
curl -X POST http://localhost:8000/store/carts/17eed084.../items/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

#### 5. Update Item Quantity
```bash
curl -X PATCH http://localhost:8000/store/carts/17eed084.../items/1/ \
  -H "Content-Type: application/json" \
  -d '{"quantity": 10}'
```

#### 6. Remove Item
```bash
curl -X DELETE http://localhost:8000/store/carts/17eed084.../items/1/
```

#### 7. Clear Entire Cart
```bash
curl -X POST http://localhost:8000/store/carts/17eed084.../clear/
```

## 📋 Sample Cart Details

### Cart 9 (Simple Cart - $199.94)
```
• Wireless Mouse: 4x @ $29.99 = $119.96
• Denim Jeans:    1x @ $59.99 = $59.99
• Cotton T-Shirt: 1x @ $19.99 = $19.99
─────────────────────────────────────
Total:                          $199.94
```

### Cart 5 (Large Cart - $7,295.78)
```
• Wireless Mouse:          4x @ $29.99
• Laptop Pro:              5x @ $1,299.99
• Running Shoes:           4x @ $89.99
• Cotton T-Shirt:          2x @ $19.99
• Django for Beginners:    1x @ $39.99
• Mechanical Keyboard:     3x @ $129.99
• Web Development Guide:   2x @ $49.99
• Python Cookbook:         1x @ $44.99
─────────────────────────────────────
Total: 8 products, 22 items → $7,295.78
```

## 🎯 Next Steps

1. **Browse API**: Visit http://localhost:8000/store/carts/ in your browser
2. **Test Operations**: Try adding/updating/removing items
3. **Check Validations**: Try adding more items than inventory
4. **View Documentation**: See CART_API_GUIDE.md for full API reference

## 💡 Tips

- Cart IDs are UUIDs - perfect for guest checkout
- Items automatically merge if same product added twice
- All operations validate inventory availability
- Use `seed_carts` anytime to reset cart data
