// Assigned to: Mai Komar
// Phase: 2 (F2.5)
//
// TODO: Image upload component for CreateListingPage.
//
// Props:
//   - images: File[] (currently selected files)
//   - onChange(files: File[]): void (callback when files change)
//
// Structure:
//   <div className="image-upload">
//     <label className="upload-area">
//       <input type="file" multiple accept="image/*" onChange={handleFileSelect} />
//       <span>Click or drag to upload images</span>
//     </label>
//     <div className="image-previews">
//       {images.map((file, index) => (
//         <div className="image-preview" key={index}>
//           <img src={URL.createObjectURL(file)} alt={`Preview ${index}`} />
//           <button onClick={() => removeImage(index)}>&times;</button>
//         </div>
//       ))}
//     </div>
//   </div>
//
// Behavior:
//   1. Accept multiple image files (jpg, png, gif, webp)
//   2. Show thumbnail previews of selected files
//   3. Allow removing individual images (X button on each preview)
//   4. Client-side validation: max 5MB per file, only image types
//   5. Clean up object URLs on unmount to prevent memory leaks
//   6. Call onChange with updated file array whenever files are added/removed
//
// Styling: Dashed border upload area, grid of previews below
import React, { useEffect } from "react"

interface ImageUploadProps {
  images: File[]
  onChange: (files: File[]) => void
}

export default function ImageUpload({ images, onChange }: ImageUploadProps) {
    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files
        if (files) {
            const validFiles: File[] = []
            for (let i = 0; i < files.length; i++) {
                const file = files[i]

                if (file.size > 5 * 1024 * 1024) {
                    alert(`File ${file.name} is too large (max 5MB)`)
                    continue
                }
                if (!file.type.startsWith("image/")) {
                    alert(`File ${file.name} is not an image`)
                    continue
                }
                validFiles.push(file)
            }
            onChange([...images, ...validFiles])
        }
    }

    const removeImage = (index: number) => {
        const next = [...images]
        next.splice(index, 1)
        onChange(next)
    }       

    useEffect(() => {
        return () => {
            images.forEach((file) => URL.revokeObjectURL(file.name))
        }
    }, [images])

    return (
        <div className="image-upload">
            <label className="upload-area">
                <input type="file" multiple accept="image/*" onChange={handleFileSelect} />
                <span>Click to upload images</span>
            </label>
            <div className="image-previews">
                {images.map((file, index) => (
                    <div className="image-preview" key={index}>
                        <img src={URL.createObjectURL(file)} alt={`Preview ${index}`} />
                        <button onClick={() => removeImage(index)}>&times;</button>
                    </div>
                ))}
            </div>
        </div>
    )
}