from datetime import datetime
import os

FILE_NAME = "data_baoduong.txt"
VALID_STATUSES = ("Đang sửa", "Chờ phụ tùng", "Hoàn thành", "Đã bàn giao")
MAINTENANCE_THRESHOLDS = {
    "Xe máy": 5000.0,
    "Ô tô": 10000.0,
    "Mặc định": 8000.0,
}


def parse_date(date_str):
    """Chuyển chuỗi YYYY-MM-DD sang đối tượng datetime.date, trả về None nếu sai định dạng."""
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def input_non_empty(prompt):
    """Yêu cầu nhập chuỗi không được bỏ trống."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  [Lỗi] Thông tin bắt buộc, không được để trống. Vui lòng nhập lại!")


def input_non_negative_float(prompt):
    """Yêu cầu nhập số thực không âm, bắt ngoại lệ ValueError."""
    while True:
        raw = input(prompt).strip()
        try:
            val = float(raw)
            if val < 0:
                print("  [Lỗi] Giá trị phải lớn hơn hoặc bằng 0. Vui lòng nhập lại!")
                continue
            return val
        except ValueError:
            print("  [Lỗi] Nhập sai kiểu dữ liệu! Vui lòng nhập một số hợp lệ.")


def input_valid_date(prompt):
    """Yêu cầu nhập ngày hợp lệ theo định dạng YYYY-MM-DD."""
    while True:
        raw = input(prompt).strip()
        if parse_date(raw) is not None:
            return raw
        print("  [Lỗi] Ngày không hợp lệ! Vui lòng nhập đúng định dạng YYYY-MM-DD (VD: 2026-11-18).")


def input_status(prompt="Chọn trạng thái (1-Đang sửa, 2-Chờ phụ tùng, 3-Hoàn thành, 4-Đã bàn giao): "):
    """Chọn trạng thái hợp lệ từ danh mục cố định."""
    while True:
        choice = input(prompt).strip()
        if choice in ("1", "2", "3", "4"):
            return VALID_STATUSES[int(choice) - 1]
        print("  [Lỗi] Lựa chọn trạng thái không hợp lệ (chỉ nhập 1, 2, 3 hoặc 4).")


def is_duplicate_ticket(records, ma_phieu):
    """Kiểm tra mã phiếu sửa chữa đã tồn tại trong danh sách hay chưa."""
    code = ma_phieu.strip().upper()
    for item in records:
        if item["ma_phieu"].upper() == code:
            return True
    return False


def find_record_by_ticket(records, ma_phieu):
    """Tìm và trả về bản ghi theo mã phiếu sửa chữa (không phân biệt hoa thường)."""
    code = ma_phieu.strip().upper()
    for item in records:
        if item["ma_phieu"].upper() == code:
            return item
    return None


def calculate_total_cost(chi_phi_phu_tung, chi_phi_cong):
    """Tính tổng chi phí = chi phí phụ tùng + chi phí công."""
    return round(chi_phi_phu_tung + chi_phi_cong, 2)


def add_record(records):
    """Chức năng 1: Thêm một phiếu bảo dưỡng / sửa chữa xe mới."""
    print("\n--- THÊM PHIẾU BẢO DƯỠNG / SỬA CHỮA MỚI ---")
    while True:
        ma_phieu = input_non_empty("Nhập mã phiếu sửa chữa (VD: PSC016): ").upper()
        if is_duplicate_ticket(records, ma_phieu):
            print(f"  [Lỗi] Mã phiếu '{ma_phieu}' đã tồn tại! Vui lòng nhập mã khác.")
        else:
            break

    ma_phuong_tien = input_non_empty("Nhập mã phương tiện (VD: PT016): ").upper()
    bien_so_xe = input_non_empty("Nhập biển số xe (VD: 30A-686.86): ").upper()
    chu_phuong_tien = input_non_empty("Nhập họ tên chủ phương tiện: ")
    so_dien_thoai = input_non_empty("Nhập số điện thoại liên hệ: ")
    loai_xe = input_non_empty("Nhập loại xe (Ô tô / Xe máy / Xe tải): ")
    so_km_hien_tai = input_non_negative_float("Nhập số kilomet hiện tại (km): ")

    ngay_tiep_nhan = input_valid_date("Nhập ngày tiếp nhận (YYYY-MM-DD): ")
    while True:
        ngay_du_kien = input_valid_date("Nhập ngày dự kiến hoàn thành (YYYY-MM-DD): ")
        if parse_date(ngay_du_kien) < parse_date(ngay_tiep_nhan):
            print("  [Lỗi] Ngày dự kiến hoàn thành không được trước ngày tiếp nhận!")
        else:
            break

    chi_phi_phu_tung = input_non_negative_float("Nhập chi phí phụ tùng (VNĐ): ")
    chi_phi_cong = input_non_negative_float("Nhập chi phí công thợ (VNĐ): ")
    tong_chi_phi = calculate_total_cost(chi_phi_phu_tung, chi_phi_cong)
    trang_thai = input_status()

    new_item = {
        "ma_phieu": ma_phieu,
        "ma_phuong_tien": ma_phuong_tien,
        "bien_so_xe": bien_so_xe,
        "chu_phuong_tien": chu_phuong_tien,
        "so_dien_thoai": so_dien_thoai,
        "loai_xe": loai_xe,
        "so_km_hien_tai": so_km_hien_tai,
        "ngay_tiep_nhan": ngay_tiep_nhan,
        "ngay_du_kien": ngay_du_kien,
        "chi_phi_phu_tung": chi_phi_phu_tung,
        "chi_phi_cong": chi_phi_cong,
        "tong_chi_phi": tong_chi_phi,
        "trang_thai": trang_thai,
    }
    records.append(new_item)
    print(f"  [Thành công] Đã thêm phiếu '{ma_phieu}' (Tổng chi phí: {tong_chi_phi:,.0f} VNĐ).")


def display_records(records, title="DANH SÁCH PHIẾU BẢO DƯỠNG & SỬA CHỮA XE"):
    """Chức năng 2: Hiển thị toàn bộ danh sách dưới dạng bảng căn cột rõ ràng."""
    print(f"\n=== {title} ({len(records)} bản ghi) ===")
    if not records:
        print("  (Danh sách hiện đang trống)")
        return

    header = (
        f"{'Mã Phiếu':<8} | {'Mã PT':<6} | {'Biển Số':<11} | {'Chủ Phương Tiện':<18} | "
        f"{'Loại Xe':<9} | {'Số KM':>8} | {'Tiếp Nhận':<10} | {'Tổng Chi Phí':>13} | {'Trạng Thái':<12}"
    )
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    for r in records:
        print(
            f"{r['ma_phieu']:<8} | {r['ma_phuong_tien']:<6} | {r['bien_so_xe']:<11} | "
            f"{r['chu_phuong_tien']:<18} | {r['loai_xe']:<9} | {r['so_km_hien_tai']:>8,.0f} | "
            f"{r['ngay_tiep_nhan']:<10} | {r['tong_chi_phi']:>13,.0f} | {r['trang_thai']:<12}"
        )
    print("-" * len(header))


def update_record(records):
    """Chức năng 3: Cập nhật thông tin theo mã phiếu sửa chữa."""
    print("\n--- CẬP NHẬT THÔNG TIN PHIẾU SỬA CHỮA ---")
    if not records:
        print("  [Thông báo] Danh sách trống, không có dữ liệu để cập nhật.")
        return

    ma_phieu = input_non_empty("Nhập mã phiếu sửa chữa cần cập nhật: ").upper()
    item = find_record_by_ticket(records, ma_phieu)
    if item is None:
        print(f"  [Lỗi] Không tìm thấy phiếu sửa chữa có mã '{ma_phieu}'.")
        return

    print(f"Đang cập nhật phiếu {item['ma_phieu']} - Xe {item['bien_so_xe']} (Nhấn Enter để giữ nguyên):")
    new_owner = input(f"  Chủ phương tiện [{item['chu_phuong_tien']}]: ").strip()
    if new_owner:
        item["chu_phuong_tien"] = new_owner

    new_phone = input(f"  Số điện thoại [{item['so_dien_thoai']}]: ").strip()
    if new_phone:
        item["so_dien_thoai"] = new_phone

    while True:
        raw_km = input(f"  Số kilomet hiện tại [{item['so_km_hien_tai']:,.0f}]: ").strip()
        if not raw_km:
            break
        try:
            val_km = float(raw_km)
            if val_km < 0:
                print("  [Lỗi] Số kilomet không được âm!")
                continue
            item["so_km_hien_tai"] = val_km
            break
        except ValueError:
            print("  [Lỗi] Vui lòng nhập số hợp lệ!")

    while True:
        raw_due = input(f"  Ngày dự kiến hoàn thành [{item['ngay_du_kien']}]: ").strip()
        if not raw_due:
            break
        d_due = parse_date(raw_due)
        if d_due is None:
            print("  [Lỗi] Sai định dạng YYYY-MM-DD!")
        elif d_due < parse_date(item["ngay_tiep_nhan"]):
            print("  [Lỗi] Ngày dự kiến không được trước ngày tiếp nhận!")
        else:
            item["ngay_du_kien"] = raw_due
            break

    while True:
        raw_pt = input(f"  Chi phí phụ tùng [{item['chi_phi_phu_tung']:,.0f}]: ").strip()
        if not raw_pt:
            break
        try:
            val_pt = float(raw_pt)
            if val_pt < 0:
                print("  [Lỗi] Chi phí không được âm!")
                continue
            item["chi_phi_phu_tung"] = val_pt
            break
        except ValueError:
            print("  [Lỗi] Vui lòng nhập số hợp lệ!")

    while True:
        raw_cong = input(f"  Chi phí công [{item['chi_phi_cong']:,.0f}]: ").strip()
        if not raw_cong:
            break
        try:
            val_cong = float(raw_cong)
            if val_cong < 0:
                print("  [Lỗi] Chi phí không được âm!")
                continue
            item["chi_phi_cong"] = val_cong
            break
        except ValueError:
            print("  [Lỗi] Vui lòng nhập số hợp lệ!")

    item["tong_chi_phi"] = calculate_total_cost(item["chi_phi_phu_tung"], item["chi_phi_cong"])

    change_st = input(f"  Đổi trạng thái hiện tại ({item['trang_thai']})? (y/n): ").strip().lower()
    if change_st == "y":
        item["trang_thai"] = input_status()

    print(f"  [Thành công] Đã cập nhật phiếu '{ma_phieu}'. Tổng chi phí mới: {item['tong_chi_phi']:,.0f} VNĐ.")


def delete_record(records):
    """Chức năng 4: Xóa bản ghi theo mã phiếu sửa chữa (có xác nhận)."""
    print("\n--- XÓA PHIẾU BẢO DƯỠNG / SỬA CHỮA ---")
    if not records:
        print("  [Thông báo] Danh sách trống, không có dữ liệu để xóa.")
        return

    ma_phieu = input_non_empty("Nhập mã phiếu sửa chữa cần xóa: ").upper()
    item = find_record_by_ticket(records, ma_phieu)
    if item is None:
        print(f"  [Lỗi] Không tìm thấy phiếu sửa chữa có mã '{ma_phieu}'.")
        return

    confirm = input(
        f"Bạn có chắc chắn muốn xóa phiếu '{item['ma_phieu']}' (Xe {item['bien_so_xe']} - {item['chu_phuong_tien']})? (y/n): "
    ).strip().lower()
    if confirm == "y":
        records.remove(item)
        print(f"  [Thành công] Đã xóa phiếu '{ma_phieu}' khỏi hệ thống.")
    else:
        print("  [Hủy bỏ] Đã giữ nguyên dữ liệu.")


def search_records(records):
    """Chức năng 5: Tìm kiếm theo biển số xe, chủ phương tiện hoặc mã phiếu sửa chữa."""
    print("\n--- TÌM KIẾM THÔNG TIN BẢO DƯỠNG / SỬA CHỮA ---")
    if not records:
        print("  [Thông báo] Danh sách hiện đang trống.")
        return

    print("1. Tìm theo biển số xe")
    print("2. Tìm theo chủ phương tiện")
    print("3. Tìm theo mã phiếu sửa chữa")
    choice = input("Chọn tiêu chí tìm kiếm (1-3): ").strip()

    if choice not in ("1", "2", "3"):
        print("  [Lỗi] Tiêu chí tìm kiếm không hợp lệ!")
        return

    keyword = input_non_empty("Nhập từ khóa tìm kiếm: ").lower()
    results = []
    for r in records:
        if choice == "1" and keyword in r["bien_so_xe"].lower():
            results.append(r)
        elif choice == "2" and keyword in r["chu_phuong_tien"].lower():
            results.append(r)
        elif choice == "3" and keyword in r["ma_phieu"].lower():
            results.append(r)

    if results:
        display_records(results, title=f"KẾT QUẢ TÌM KIẾM CHO '{keyword.upper()}'")
    else:
        print(f"  [Thông báo] Không tìm thấy bản ghi nào phù hợp với từ khóa '{keyword}'.")


def sort_records(records):
    """Chức năng 6: Sắp xếp theo ngày tiếp nhận hoặc tổng chi phí (tăng/giảm dần)."""
    print("\n--- SẮP XẾP DANH SÁCH PHIẾU SỬA CHỮA ---")
    if not records:
        print("  [Thông báo] Danh sách trống, không thể sắp xếp.")
        return

    print("1. Sắp xếp theo ngày tiếp nhận")
    print("2. Sắp xếp theo tổng chi phí")
    criterion = input("Chọn tiêu chí sắp xếp (1-2): ").strip()
    if criterion not in ("1", "2"):
        print("  [Lỗi] Tiêu chí sắp xếp không hợp lệ!")
        return

    print("1. Tăng dần")
    print("2. Giảm dần")
    order = input("Chọn thứ tự sắp xếp (1-2): ").strip()
    if order not in ("1", "2"):
        print("  [Lỗi] Thứ tự sắp xếp không hợp lệ!")
        return

    reverse_flag = (order == "2")
    if criterion == "1":
        records.sort(key=lambda x: x["ngay_tiep_nhan"], reverse=reverse_flag)
        label = "NGÀY TIẾP NHẬN"
    else:
        records.sort(key=lambda x: x["tong_chi_phi"], reverse=reverse_flag)
        label = "TỔNG CHI PHÍ"

    order_label = "GIẢM DẦN" if reverse_flag else "TĂNG DẦN"
    display_records(records, title=f"DANH SÁCH SAU KHI SẮP XẾP THEO {label} ({order_label})")


def calculate_and_statistics(records, ref_date_str="2026-11-18"):
    """Chức năng 7: Tính toán nghiệp vụ và thống kê toàn diện."""
    print("\n================ BÁO CÁO TÍNH TOÁN & THỐNG KÊ ================")
    if not records:
        print("  [Thông báo] Chưa có dữ liệu để thống kê.")
        return

    today = parse_date(ref_date_str) if ref_date_str else datetime.now().date()

    total_revenue = 0.0
    in_progress_or_overdue = []
    due_for_maintenance = []

    for r in records:
        r["tong_chi_phi"] = calculate_total_cost(r["chi_phi_phu_tung"], r["chi_phi_cong"])
        total_revenue += r["tong_chi_phi"]

        is_unfinished = r["trang_thai"] in ("Đang sửa", "Chờ phụ tùng")
        is_overdue = is_unfinished and (parse_date(r["ngay_du_kien"]) < today)
        if is_unfinished or is_overdue:
            in_progress_or_overdue.append((r, is_overdue))

        loai_lower = r["loai_xe"].lower()
        if "xe máy" in loai_lower or "tay ga" in loai_lower or "xe số" in loai_lower:
            threshold = MAINTENANCE_THRESHOLDS["Xe máy"]
        elif "ô tô" in loai_lower or "xe tải" in loai_lower:
            threshold = MAINTENANCE_THRESHOLDS["Ô tô"]
        else:
            threshold = MAINTENANCE_THRESHOLDS["Mặc định"]

        if r["so_km_hien_tai"] >= threshold:
            due_for_maintenance.append((r, threshold))

    avg_cost = total_revenue / len(records)

    print(f"1. Tổng số phiếu bảo dưỡng/sửa chữa : {len(records)} phiếu")
    print(f"2. Tổng doanh thu sửa chữa          : {total_revenue:,.0f} VNĐ")
    print(f"3. Chi phí sửa chữa trung bình      : {avg_cost:,.0f} VNĐ / phiếu")

    print(f"\n4. Danh sách xe ĐANG SỬA hoặc QUÁ HẠN DỰ KIẾN ({len(in_progress_or_overdue)} xe):")
    if not in_progress_or_overdue:
        print("   -> Không có xe nào đang sửa hoặc quá hạn.")
    else:
        for r, overdue in in_progress_or_overdue:
            note = " [QUÁ HẠN DỰ KIẾN!]" if overdue else ""
            print(
                f"   - {r['ma_phieu']} | {r['bien_so_xe']} ({r['chu_phuong_tien']}) | "
                f"Trạng thái: {r['trang_thai']} | Dự kiến xong: {r['ngay_du_kien']}{note}"
            )

    print(f"\n5. Cảnh báo xe ĐẾN HẠN BẢO DƯỠNG theo số KM định kỳ ({len(due_for_maintenance)} xe):")
    if not due_for_maintenance:
        print("   -> Không có xe nào vượt ngưỡng kilomet bảo dưỡng.")
    else:
        for r, th in due_for_maintenance:
            print(
                f"   - {r['bien_so_xe']} ({r['loai_xe']} - Chủ xe: {r['chu_phuong_tien']}): "
                f"{r['so_km_hien_tai']:,.0f} km (Mốc định kỳ: {th:,.0f} km)"
            )
    print("===============================================================")


def save_to_file(records, filename=FILE_NAME):
    """Chức năng 8: Lưu danh sách phiếu bảo dưỡng/sửa chữa xuống file TXT."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for r in records:
                line = "|".join([
                    r["ma_phieu"],
                    r["ma_phuong_tien"],
                    r["bien_so_xe"],
                    r["chu_phuong_tien"],
                    r["so_dien_thoai"],
                    r["loai_xe"],
                    str(r["so_km_hien_tai"]),
                    r["ngay_tiep_nhan"],
                    r["ngay_du_kien"],
                    str(r["chi_phi_phu_tung"]),
                    str(r["chi_phi_cong"]),
                    str(r["tong_chi_phi"]),
                    r["trang_thai"],
                ])
                f.write(line + "\n")
        print(f"  [Thành công] Đã lưu {len(records)} bản ghi vào tệp '{filename}'.")
    except OSError as e:
        print(f"  [Lỗi] Không thể ghi dữ liệu xuống tệp '{filename}': {e}")


def load_from_file(filename=FILE_NAME):
    """Chức năng 9: Đọc dữ liệu từ file TXT và chuyển về đúng kiểu dữ liệu."""
    loaded = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 13:
                    raise ValueError(f"Dòng {line_num} không đủ 13 trường dữ liệu.")
                chi_phi_pt = float(parts[9])
                chi_phi_c = float(parts[10])
                record = {
                    "ma_phieu": parts[0].strip(),
                    "ma_phuong_tien": parts[1].strip(),
                    "bien_so_xe": parts[2].strip(),
                    "chu_phuong_tien": parts[3].strip(),
                    "so_dien_thoai": parts[4].strip(),
                    "loai_xe": parts[5].strip(),
                    "so_km_hien_tai": float(parts[6]),
                    "ngay_tiep_nhan": parts[7].strip(),
                    "ngay_du_kien": parts[8].strip(),
                    "chi_phi_phu_tung": chi_phi_pt,
                    "chi_phi_cong": chi_phi_c,
                    "tong_chi_phi": calculate_total_cost(chi_phi_pt, chi_phi_c),
                    "trang_thai": parts[12].strip(),
                }
                loaded.append(record)
        print(f"  [Thành công] Đã đọc {len(loaded)} bản ghi từ tệp '{filename}'.")
        return loaded
    except FileNotFoundError:
        print(f"  [Cảnh báo] Tệp '{filename}' không tồn tại! Khởi tạo danh sách trống.")
        return []
    except (ValueError, OSError) as e:
        print(f"  [Lỗi] Không thể đọc dữ liệu từ tệp '{filename}': {e}")
        return []


def show_menu():
    """Hiển thị menu điều khiển chương trình."""
    print("\n============================================================")
    print("      CHƯƠNG TRÌNH QUẢN LÝ BẢO DƯỠNG VÀ SỬA CHỮA XE")
    print("============================================================")
    print("1. Thêm")
    print("2. Hiển thị danh sách")
    print("3. Cập nhật")
    print("4. Xóa")
    print("5. Tìm kiếm")
    print("6. Sắp xếp")
    print("7. Tính toán/Thống kê")
    print("8. Lưu dữ liệu")
    print("9. Đọc dữ liệu")
    print("0. Thoát")
    print("============================================================")


def main():
    """Hàm điều khiển luồng chạy chính của chương trình."""
    records = load_from_file(FILE_NAME)
    while True:
        show_menu()
        choice = input("Lựa chọn: ").strip()
        if choice == "1":
            add_record(records)
        elif choice == "2":
            display_records(records)
        elif choice == "3":
            update_record(records)
        elif choice == "4":
            delete_record(records)
        elif choice == "5":
            search_records(records)
        elif choice == "6":
            sort_records(records)
        elif choice == "7":
            calculate_and_statistics(records)
        elif choice == "8":
            save_to_file(records, FILE_NAME)
        elif choice == "9":
            records = load_from_file(FILE_NAME)
        elif choice == "0":
            print("Đã thoát chương trình. Hẹn gặp lại!")
            break
        else:
            print("  [Lỗi] Lựa chọn không hợp lệ! Vui lòng chọn từ 0 đến 9.")


if __name__ == "__main__":
    main()