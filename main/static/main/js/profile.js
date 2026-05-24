const contactDialog = document.getElementById("contact-dialog");
const openContact = document.getElementById("open-contact");
const closeContact = document.getElementById("close-contact");
const cancelContact = document.getElementById("cancel-contact");
const avatarForm = document.querySelector(".avatar-form");
const avatarButton = document.getElementById("avatar-button");
const avatarInput = document.getElementById("avatar-input");
const avatarData = document.getElementById("avatar-data");
const avatarPreview = document.getElementById("avatar-preview");

if (openContact && contactDialog) {
  openContact.addEventListener("click", () => {
    contactDialog.showModal();
  });
}

if (closeContact && contactDialog) {
  closeContact.addEventListener("click", () => {
    contactDialog.close();
  });
}

if (cancelContact && contactDialog) {
  cancelContact.addEventListener("click", () => {
    contactDialog.close();
  });
}

if (avatarButton && avatarInput && avatarData && avatarForm && avatarPreview) {
  avatarButton.addEventListener("click", () => {
    avatarInput.click();
  });

  avatarInput.addEventListener("change", () => {
    const file = avatarInput.files[0];

    if (!file || !file.type.startsWith("image/")) {
      return;
    }

    const reader = new FileReader();

    reader.addEventListener("load", () => {
      const image = new Image();

      image.addEventListener("load", () => {
        const size = 320;
        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");
        const side = Math.min(image.width, image.height);
        const sourceX = (image.width - side) / 2;
        const sourceY = (image.height - side) / 2;

        canvas.width = size;
        canvas.height = size;
        context.drawImage(image, sourceX, sourceY, side, side, 0, 0, size, size);

        avatarData.value = canvas.toDataURL("image/jpeg", 0.86);
        avatarPreview.src = avatarData.value;
        avatarPreview.hidden = false;
        avatarForm.submit();
      });

      image.src = reader.result;
    });

    reader.readAsDataURL(file);
  });
}
