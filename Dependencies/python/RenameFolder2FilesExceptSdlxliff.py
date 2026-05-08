import os
import shutil

def rename_files_with_parent_folder(dry_run=False):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    for item in os.listdir(script_dir):
        item_path = os.path.join(script_dir, item)
        
        if not os.path.isdir(item_path):
            continue  # Skip non-folders
        
        parent_folder_name = os.path.basename(item_path)
        
        for root, _, files in os.walk(item_path):
            for file in files:
                # Skip .sdxliff files entirely
                if file.endswith(".sdlxliff"):
                    print(f"Skipping .sdlxliff file: {os.path.join(root, file)}")
                    continue
                
                # Skip if already renamed
                if f"_{parent_folder_name}." in file:
                    print(f"Skipping (already renamed): {os.path.join(root, file)}")
                    continue
                
                # Split filename and extension properly
                file_base, file_ext = os.path.splitext(file)
                new_name = f"{file_base}_{parent_folder_name}{file_ext}"
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_name)
                
                if dry_run:
                    print(f"[DRY RUN] Would rename: {old_path} → {new_path}")
                else:
                    shutil.move(old_path, new_path)
                    print(f"Renamed: {old_path} → {new_path}")

if __name__ == "__main__":
    # Set dry_run=True to preview changes first
    rename_files_with_parent_folder(dry_run=False)
    print("✅ All files renamed (except .sdlxliff)!")