"""برنامج كاشير بسيط يعمل عبر سطر الأوامر."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Item:
    name: str
    price: float
    quantity: int

    @property
    def subtotal(self) -> float:
        return self.price * self.quantity


def ask_float(prompt: str, minimum: float = 0.0) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value < minimum:
                print(f"⚠️  القيمة يجب أن تكون أكبر من أو تساوي {minimum}")
                continue
            return value
        except ValueError:
            print("⚠️  يرجى إدخال رقم صحيح.")


def ask_int(prompt: str, minimum: int = 1) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value < minimum:
                print(f"⚠️  القيمة يجب أن تكون أكبر من أو تساوي {minimum}")
                continue
            return value
        except ValueError:
            print("⚠️  يرجى إدخال عدد صحيح.")


def print_cart(cart: list[Item]) -> None:
    if not cart:
        print("\n🛒 السلة فارغة.\n")
        return

    print("\n--- محتويات السلة ---")
    print(f"{'المنتج':<20}{'السعر':>10}{'الكمية':>10}{'الإجمالي':>12}")
    print("-" * 52)
    for item in cart:
        print(f"{item.name:<20}{item.price:>10.2f}{item.quantity:>10}{item.subtotal:>12.2f}")
    print("-" * 52)
    total = sum(item.subtotal for item in cart)
    print(f"{'المجموع':<40}{total:>12.2f}\n")


def checkout(cart: list[Item], vat_percent: float = 15.0) -> None:
    if not cart:
        print("\n⚠️  لا يمكن إنهاء البيع لأن السلة فارغة.\n")
        return

    subtotal = sum(item.subtotal for item in cart)
    discount = ask_float("أدخل قيمة الخصم (0 إذا لا يوجد): ", minimum=0.0)
    discount = min(discount, subtotal)

    taxable = subtotal - discount
    vat_amount = taxable * (vat_percent / 100)
    total = taxable + vat_amount

    paid = ask_float("المبلغ المدفوع: ", minimum=total)
    change = paid - total

    print("\n===== الفاتورة =====")
    print_cart(cart)
    print(f"المجموع الفرعي: {subtotal:.2f}")
    print(f"الخصم: {discount:.2f}")
    print(f"الضريبة ({vat_percent:.0f}%): {vat_amount:.2f}")
    print(f"الإجمالي النهائي: {total:.2f}")
    print(f"المدفوع: {paid:.2f}")
    print(f"الباقي: {change:.2f}")
    print("===================\n")

    save = input("هل تريد حفظ الفاتورة في ملف؟ (y/n): ").strip().lower()
    if save == "y":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"receipt_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("فاتورة كاشير\n")
            f.write("=" * 30 + "\n")
            for item in cart:
                f.write(
                    f"{item.name} | سعر: {item.price:.2f} | كمية: {item.quantity} | إجمالي: {item.subtotal:.2f}\n"
                )
            f.write("-" * 30 + "\n")
            f.write(f"المجموع الفرعي: {subtotal:.2f}\n")
            f.write(f"الخصم: {discount:.2f}\n")
            f.write(f"الضريبة: {vat_amount:.2f}\n")
            f.write(f"الإجمالي النهائي: {total:.2f}\n")
            f.write(f"المدفوع: {paid:.2f}\n")
            f.write(f"الباقي: {change:.2f}\n")
        print(f"✅ تم حفظ الفاتورة في {filename}")

    cart.clear()
    print("✅ تم إنهاء عملية البيع وتفريغ السلة.\n")


def main() -> None:
    cart: list[Item] = []

    print("أهلاً بك في برنامج الكاشير البسيط")
    while True:
        print("""
اختر عملية:
1) إضافة منتج
2) عرض السلة
3) إنهاء البيع
4) خروج
""")
        choice = input("اختيارك: ").strip()

        if choice == "1":
            name = input("اسم المنتج: ").strip()
            if not name:
                print("⚠️  اسم المنتج لا يمكن أن يكون فارغاً.")
                continue
            price = ask_float("سعر المنتج: ", minimum=0.01)
            quantity = ask_int("الكمية: ", minimum=1)
            cart.append(Item(name=name, price=price, quantity=quantity))
            print("✅ تمت إضافة المنتج بنجاح.\n")
        elif choice == "2":
            print_cart(cart)
        elif choice == "3":
            checkout(cart)
        elif choice == "4":
            print("👋 شكراً لاستخدامك البرنامج.")
            break
        else:
            print("⚠️  اختيار غير صحيح، حاول مرة أخرى.")


if __name__ == "__main__":
    main()
