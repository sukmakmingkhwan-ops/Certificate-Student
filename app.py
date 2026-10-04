import io
import fitz  # PyMuPDF
import streamlit as st

st.set_page_config(
    page_title="ค้นหาเกียรติบัตร",
    page_icon="📜",
    layout="centered",
)
st.title("📜 ระบบค้นหาและดาวน์โหลดเกียรติบัตร")

# รายชื่อไฟล์ PDF ทั้งหมด 8 งาน (job1 - job8)
PDF_FILES = [
    "job1.pdf",
    "job2.pdf",
    "job3.pdf",
    "job4.pdf",
    "job5.pdf",
    "job6.pdf",
    "job7.pdf",
    "job8.pdf",
]

# ช่องกรอกค้นหาชื่อ-นามสกุล
search_name = st.text_input("กรอกชื่อ-นามสกุล ที่ต้องการค้นหา:")

if st.button("🔍 ค้นหาเกียรติบัตร"):
    clean_name = search_name.replace(" ", "").strip()

    if not clean_name:
        st.warning("กรุณากรอกชื่อ-นามสกุลก่อนกดค้นหา")
    else:
        total_found = 0

        # ค้นหาข้อความจากทั้ง 8 ไฟล์
        for pdf_file in PDF_FILES:
            try:
                doc = fitz.open(pdf_file)
            except Exception:
                continue

            for page_index in range(len(doc)):
                page = doc[page_index]
                page_text = page.get_text().replace(" ", "").strip()

                if clean_name in page_text:
                    total_found += 1

                    # แปลงหน้า PDF เป็นภาพตัวอย่าง Preview (150 dpi)
                    pix = page.get_pixmap(dpi=150)
                    img_bytes = pix.tobytes("png")

                    st.markdown(f"### 📄 เกียรติบัตรใบที่ {total_found}")
                    st.image(
                        img_bytes,
                        caption=f"หน้า {page_index + 1}",
                        use_container_width=True,
                    )

                    # สร้างไฟล์ PDF สำหรับดาวน์โหลดเฉพาะใบ
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
                f"ไม่พบชื่อ '{search_name}' ในระบบ โปรดตรวจสอบตัวสะกดอีกครั้ง"
            )
        else:
            st.success(f"พบเกียรติบัตรทั้งหมด {total_found} รายการ")
