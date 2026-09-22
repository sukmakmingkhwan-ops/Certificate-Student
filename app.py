import io
import os
import fitz  # PyMuPDF
import streamlit as st

# ปรับชื่อหน้าเว็บตามโครงการใหม่
st.set_page_config(page_title="ค้นหาเกียรติบัตร โครงการใหม่", page_icon="📜", layout="centered")
st.title("📜 ระบบค้นหาและดาวน์โหลดเกียรติบัตร (โครงการใหม่)")

# รายชื่อกิจกรรมและไฟล์ PDF ของโครงการใหม่
ACTIVITIES = {
    "กิจกรรมที่ 1: ชื่องานกิจกรรมที่ 1": "activity1.pdf",
    "กิจกรรมที่ 2: ชื่องานกิจกรรมที่ 2": "activity2.pdf",
}

selected_activity = st.selectbox("1. กรุณาเลือกกิจกรรม / โครงการ:", list(ACTIVITIES.keys()))
pdf_path = ACTIVITIES[selected_activity]

search_name = st.text_input("2. กรอกชื่อ-นามสกุล ที่ต้องการค้นหา:")

if st.button("🔍 ค้นหาเกียรติบัตร"):
    if not os.path.exists(pdf_path):
        st.error(f"ไม่พบไฟล์เกียรติบัตร '{pdf_path}' ในระบบ")
    elif not search_name.strip():
        st.warning("กรุณากรอกชื่อก่อนกดค้นหา")
    else:
        doc = fitz.open(pdf_path)
        clean_search = search_name.replace(" ", "").strip()
        matched_pages = []

        for page_index in range(len(doc)):
            page_text = doc[page_index].get_text().replace(" ", "").strip()
            if clean_search in page_text:
                matched_pages.append(page_index)

        if matched_pages:
            st.success(f"พบเกียรติบัตรของคุณใน '{selected_activity}' ทั้งหมด {len(matched_pages)} รายการ")

            for idx, p in enumerate(matched_pages, start=1):
                page = doc[p]
                pix = page.get_pixmap(dpi=150)
                img_bytes = pix.tobytes("png")

                st.markdown(f"### 📄 เกียรติบัตรใบที่ {idx}")
                st.image(img_bytes, caption=f"หน้า {p + 1}", use_container_width=True)

                single_doc = fitz.open()
                single_doc.insert_pdf(doc, from_page=p, to_page=p)

                pdf_buffer = io.BytesIO()
                single_doc.save(pdf_buffer)
                single_doc.close()

                clean_act_name = selected_activity.split(":")[0].strip()
                st.download_button(
                    label=f"⬇️ ดาวน์โหลดเกียรติบัตรใบที่ {idx} (.pdf)",
                    data=pdf_buffer.getvalue(),
                    file_name=f"เกียรติบัตร_{clean_act_name}_{search_name.strip()}_ใบที่{idx}.pdf",
                    mime="application/pdf",
                    key=f"download_{p}_{idx}"
                )
                st.divider()

            if len(matched_pages) > 1:
                all_doc = fitz.open()
                for p in matched_pages:
                    all_doc.insert_pdf(doc, from_page=p, to_page=p)

                all_buffer = io.BytesIO()
                all_doc.save(all_buffer)
                all_doc.close()

                st.download_button(
                    label="📦 ดาวน์โหลดเกียรติบัตรทั้งหมดรวมกัน (PDF)",
                    data=all_buffer.getvalue(),
                    file_name=f"เกียรติบัตร_{clean_act_name}_{search_name.strip()}_ทั้งหมด.pdf",
                    mime="application/pdf",
                    key="download_all"
                )
        else:
            st.error(f"ไม่พบชื่อ '{search_name}' ในกิจกรรมนี้ โปรดตรวจสอบตัวสะกด")

        doc.close()