# Real Estate Backend API Documentation

## Base URL
```
https://your-api-domain.com/api
```

## Authentication
All endpoints require authentication (to be implemented).

## Endpoints

### Upload Property Images
Upload multiple images for a property.

```
POST /properties/{property_id}/images
```

**Request**
- Content-Type: multipart/form-data

| Parameter | Type | Description |
|-----------|------|-------------|
| files | File[] | Array of image files to upload |

**Response**
```json
[
    {
        "id": "image_id_1",
        "storage_url": "https://storage.url/image1.jpg",
        "filename": "CP00001-01.jpg",
        "title": "",
        "description": "",
        "order": 1,
        "created_at": "2025-02-04T12:00:00Z"
    },
    {
        "id": "image_id_2",
        "storage_url": "https://storage.url/image2.jpg",
        "filename": "CP00001-02.jpg",
        "title": "",
        "description": "",
        "order": 2,
        "created_at": "2025-02-04T12:00:00Z"
    }
]
```

**Error Response**
```json
{
    "error": "Error message description"
}
```

### Update Image Metadata
Update title and description for a specific image.

```
PUT /properties/{property_id}/images/{image_id}
```

**Request Body**
```json
{
    "title": "Beautiful Kitchen",
    "description": "Modern kitchen with granite countertops"
}
```

**Response**
```json
{
    "title": "Beautiful Kitchen",
    "description": "Modern kitchen with granite countertops"
}
```

### Update Image Collections
Update featured, interior, and exterior image collections.

```
PUT /properties/{property_id}/collections
```

**Request Body**
```json
{
    "feature_image_id": "image_id_1",
    "interior_image_ids": ["image_id_2", "image_id_3"],
    "exterior_image_ids": ["image_id_4", "image_id_5"]
}
```

**Response**
```json
{
    "feature_image_id": "image_id_1",
    "interior_image_ids": ["image_id_2", "image_id_3"],
    "exterior_image_ids": ["image_id_4", "image_id_5"]
}
```

## Image Processing Specifications

### Image Standards
- Resolution: 800x600 pixels
- Format: JPEG
- Quality: 85%
- Maximum upload size: 10MB per image
- Accepted formats: jpg, jpeg, png

### File Naming Convention
Format: `{property_id}-{XX}.jpg`
- property_id: Property reference number
- XX: Two-digit sequential number (01-99)

Example: `CP00001-01.jpg`

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 413 | Payload Too Large - File size exceeds limit |
| 415 | Unsupported Media Type - Invalid file format |
| 500 | Internal Server Error |

## Usage Examples

### Upload Images Using cURL
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg" \
  https://your-api-domain.com/api/properties/CP00001/images
```

### Update Image Metadata Using cURL
```bash
curl -X PUT \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Master Bedroom", "description": "Spacious master bedroom"}' \
  https://your-api-domain.com/api/properties/CP00001/images/image_id_1
```

### Update Collections Using cURL
```bash
curl -X PUT \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"feature_image_id": "image_id_1", "interior_image_ids": ["image_id_2"]}' \
  https://your-api-domain.com/api/properties/CP00001/collections
```

## Implementation Notes

1. Image Processing:
   - Images are automatically resized maintaining aspect ratio
   - Center cropping is applied if aspect ratio doesn't match
   - All images are converted to JPEG format
   - Optimization is applied to reduce file size

2. Collection Management:
   - Feature image can be selected from any uploaded image
   - Interior and exterior collections maintain order
   - Same image can be used in multiple collections
   - Collections are updated atomically

3. Error Handling:
   - Failed uploads don't affect successful ones
   - Invalid files are rejected with appropriate error messages
   - Concurrent uploads are supported
   - Transaction rollback on partial failures