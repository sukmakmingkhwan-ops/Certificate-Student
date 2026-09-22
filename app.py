import io
import fitz  # PyMuPDF
import streamlit as st

# 1. ตั้งค่าหน้าเว็บและหัวข้อ
st.set_page_config(
    page_title="ค้นหาเกียรติบัตรนักเรียน", page_icon="📜", layout="centered"
)
st.title("📜 ระบบค้นหาและดาวน์โหลดเกียรติบัตร")

# 2. ระบุรายชื่อไฟล์ PDF ทั้งหมดในระบบ (ระบบจะค้นหาให้จากทุกไฟล์พร้อมกันอัตโนมัติ)
PDF_FILES = [
    "activity1.pdf",
    "activity2.pdf",
    "activity3.pdf",
    "activity4.pdf",
    "activity5.pdf",
    "activity6.pdf",
    "activity7.pdf",
]

# 3. ช่องให้พิมพ์ชื่อ-นามสกุลโดยตรง (ไม่ต้องมีเมนูเลือกโครงการแล้ว)
search_name = st.text_input("กรอกชื่อ-นามสกุล ที่ต้องการค้นหา:")

if st.button("🔍 ค้นหาเกียรติบัตร"):
    if not search_name.strip():
        st.warning("กรุณากรอกชื่อ-นามสกุลก่อนกดค้นหา")
    else:
        clean_search = search_name.replace(" ", "").strip()
        total_found = 0

        # วนค้นหาชื่อในไฟล์ PDF ทั้งหมด
        for pdf_file in PDF_FILES:
            try:
                doc = fitz.open(pdf_file)
            except Exception:
                continue

            for page_index in range(len(doc)):
                page = doc[page_index]
                page_text = page.get_text().replace(" ", "").strip()

                # เมื่อพบชื่อที่ตรงกัน
                if clean_search in page_text:
                    total_found += 1

                    # แปลงหน้า PDF เป็นภาพตัวอย่าง (Preview)
                    pix = page.get_pixmap(dpi=150)
                    img_bytes = pix.tobytes("png")

                    st.markdown(f"### 📄 เกียรติบัตรใบที่ {total_found}")
                    st.image(
                        img_bytes,
                        caption=f"ไฟล์: {pdf_file} (หน้า {page_index + 1})",
                        use_container_width=True,
                    )

                    # สร้างไฟล์ PDF เฉพาะหน้านี้เพื่อดาวน์โหลด
                    single_doc = fitz.open()
                    single_doc.insert_pdf(
                        doc, from_page=page_index, to_page=page_index
                    )

                    pdf_buffer = io.BytesIO()
                    single_doc.save(pdf_buffer)
                    single_doc.close()

                    st.download_button(
                        label=f"⬇️ คลิกดาวน์โหลดเกียรติบัตรใบที่ {total_found} (.pdf)",
                        data=pdf_buffer.getvalue(),
                        file_name=f"เกียรติบัตร_{search_name.strip()}_ใบที่{total_found}.pdf",
                        mime="application/pdf",
                        key=f"download_{pdf_file}_{page_index}",
                    )
                    st.divider()

            doc.close()

        if total_found == 0:
            st.error(
                f"ไม่พบชื่อ '{search_name}' ในระบบ โปรดตรวจสอบตัวสะกดชื่อ-นามสกุลอีกครั้ง"
            )
        else:
            st.success(f"พบเกียรติบัตรของคุณทั้งหมด {total_found} ใบ")
