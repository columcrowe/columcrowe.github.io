---
title: 'Reduce Disk Image Size'
description: ''
pubDate: 'Jun 25 2025'
---

**Reduce Disk Image Size**

**Notes**

-   Back up your original disk image before making changes. (as in
    backup_img.img should be a copy of your original image)

-   Changes to the loop device are reflected in the mounted image file.

-   Ensure the resized filesystem and partition sizes are compatible
    with your use case.

1.  **Attach the Disk Image to a Loop Device** Attach the disk image to
    a loop device, making it accessible as if it were a physical disk.
```bash
sudo losetup -fP /media/columcrowe/Seagate/linux/images/backup_img.img
```

2.  **Check the Assigned Loop Device** Identify the assigned loop device
    and its partitions. Make sure you identify the correct loop device
    that corresponds to your newly attached disk image (backup_img.img)
```bash
lsblk
```
> Example output:
>
> /dev/loop20 476G
>
> └─/dev/loop20p1 468G

3.  **Create a Directory for Mounting** Create a directory where the
    disk partition will be mounted.
```bash
sudo mkdir /mnt/img
```

4.  **Mount the Partition** Mount the partition (e.g., /dev/loop20p1) to
    access its contents.
```bash
sudo mount /dev/loop20p1 /mnt/img
```

5.  **Check Disk Usage** View the current usage of the mounted
    partition.
```bash
df -h /mnt/img
```
> Example output:
>
> Filesystem Size Used Avail Use% Mounted on
>
> /dev/loop20p1 468G 43G 407G 10% /mnt/img

6.  **Unmount the Partition** Unmount the partition before resizing.
```bash
sudo umount /mnt/img
```

7.  **Run Filesystem Check** Perform a filesystem check to ensure the
    partition is consistent.
```bash
sudo e2fsck -f /dev/loop20p1
```
> If prompted, confirm changes by typing y.

8.  **Resize the Filesystem** Resize the filesystem to the desired
    size - smaller than the current filesystem size (e.g., 64G). Must be
    greater than the Used size.
```bash
sudo resize2fs /dev/loop20p1 64G
```

9.  **Resize the Partition** Adjust the partition size to match the
    resized filesystem (e.g., 100G). Must be greater than resized
    filesystem size.
```bash
sudo parted /dev/loop20
```
> In the parted prompt:
>
> (parted) resizepart 1 100G
>
> (parted) quit

10. **Verify the New Partition Size** Check the partition details to
    confirm the resize.
```bash
sudo parted /dev/loop20 unit GB print
```
> Note the new size (NEW_SIZE), e.g., 100G.

11. **Detach the Loop Device Temporarily** Detach the loop device before
    resizing the image file.
```bash
sudo losetup -d /dev/loop20
```

12. **Shrink the Disk Image** Shrink the disk image file to match the
    new partition size.
```bash
sudo truncate -s NEW_SIZEG /media/columcrowe/Seagate/linux/images/backup_img.img
```
> Replace NEW_SIZE with the partition size noted earlier (e.g., 100G).

13. **Reattach the Disk Image** Reattach the resized disk image to
    verify its structure.
```bash
sudo losetup -fP /media/columcrowe/Seagate/linux/images/backup_img.img
```

14. **Verify the Disk Structure** Use gdisk to check the disk structure
    and write changes.
```bash
sudo gdisk /dev/loop20
```
> Inside gdisk:
>-   Type v to verify the structure.
>-   Type w to write changes.
>-   Confirm with Y if prompted.

15. **Detach the Loop Device** Detach the loop device after
    verification.
```bash
sudo losetup -d /dev/loop20
```

16. **Copy the Resized Disk Image to a Physical Device** Copy the
    reduced image to a physical device (e.g., /dev/sdX).
```bash
> sudo dd if=/media/columcrowe/Seagate/linux/images/backup_img.img of=/dev/sdX status=progress conv=fsync
```
> Replace /dev/sdX with the target device name.
>
> (Or use program like Balena Etcher (etc.) to flash the image.)
