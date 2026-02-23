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
