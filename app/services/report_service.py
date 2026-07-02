from datetime import date,datetime
import csv
import io
from app.repositories.visitor_application_repository import (
    VisitorApplicationRepository
)

from app.repositories.employee_repository import (
    EmployeeRepository
)

from app.repositories.department_repository import (
    DepartmentRepository
)

from app.repositories.gate_pass_repository import (
    GatePassRepository
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.units import inch

from reportlab.lib.enums import TA_CENTER

from reportlab.pdfbase import pdfmetrics

import io


class ReportService:

    def __init__(self):

        self.visitor_repository = (
            VisitorApplicationRepository()
        )

        self.employee_repository = (
            EmployeeRepository()
        )

        self.department_repository = (
            DepartmentRepository()
        )

        self.gatepass_repository = (
            GatePassRepository()
        )

    def get_dashboard_statistics(self):

        visitors = (
            self.visitor_repository
            .get_all_applications()
        )

        employees = (
            self.employee_repository
            .get_all_employees()
        )

        departments = (
            self.department_repository
            .get_all_departments()
        )

        total_visitors = len(visitors)

        total_employees = len(employees)

        total_departments = len(departments)

        active_gatepasses = (
            self.gatepass_repository
            .count_active_gatepasses()
        )

        pending = 0
        approved = 0
        rejected = 0
        today_visitors = 0

        today = str(date.today())

        for visitor in visitors:

            if visitor["status"] == "PENDING":
                pending += 1

            elif visitor["status"] == "APPROVED":
                approved += 1

            elif visitor["status"] == "REJECTED":
                rejected += 1

            visit_date = visitor.get(
                "visit_date",
                ""
            )

            if visit_date == today:
                today_visitors += 1

        return {

            "total_visitors":
                total_visitors,

            "today_visitors":
                today_visitors,

            "total_employees":
                total_employees,

            "total_departments":
                total_departments,

            "active_gatepasses":
                active_gatepasses,

            "pending":
                pending,

            "approved":
                approved,

            "rejected":
                rejected

        }

    def department_statistics(self):

        departments = (
            self.department_repository
            .get_all_departments()
        )

        visitors = (
            self.visitor_repository
            .get_all_applications()
        )

        employees = (
            self.employee_repository
            .get_all_employees()
        )

        report = []

        for department in departments:

            visitor_count = 0

            employee_count = 0

            for visitor in visitors:

                if (
                    visitor["department_id"]
                    ==
                    department["department_id"]
                ):
                    visitor_count += 1

            for employee in employees:

                if (
                    employee["department_id"]
                    ==
                    department["department_id"]
                ):
                    employee_count += 1

            report.append(

                {

                    "department_name":
                        department[
                            "department_name"
                        ],

                    "visitor_count":
                        visitor_count,

                    "employee_count":
                        employee_count

                }

            )

        return report

    def get_status_chart_data(self):

        visitors = (
            self.visitor_repository
            .get_all_applications()
        )

        pending = 0
        approved = 0
        rejected = 0

        for visitor in visitors:

            if visitor["status"] == "PENDING":
                pending += 1

            elif visitor["status"] == "APPROVED":
                approved += 1

            elif visitor["status"] == "REJECTED":
                rejected += 1

        return {

            "labels": [
                "Pending",
                "Approved",
                "Rejected"
            ],

            "values": [
                pending,
                approved,
                rejected
            ]

        }

    def get_department_chart_data(self):

        departments = (
            self.department_repository
            .get_all_departments()
        )

        visitors = (
            self.visitor_repository
            .get_all_applications()
        )

        labels = []

        values = []

        for department in departments:

            count = 0

            for visitor in visitors:

                if (
                    visitor["department_id"]
                    ==
                    department["department_id"]
                ):
                    count += 1

            labels.append(
                department["department_name"]
            )

            values.append(
                count
            )

        return {

            "labels": labels,

            "values": values

        }

    def get_daily_visitor_chart(self):

        visitors = (
            self.visitor_repository
            .get_all_applications()
        )

        daily = {}

        for visitor in visitors:

            visit_date = visitor.get(
                "visit_date"
            )

            if not visit_date:
                continue

            if visit_date not in daily:

                daily[visit_date] = 0

            daily[visit_date] += 1

        labels = list(
            daily.keys()
        )

        values = list(
            daily.values()
        )

        return {

            "labels": labels,

            "values": values

        }

    def export_visitors_csv(self):

        visitors = (
            self.visitor_repository
            .get_all_applications()
        )

        output = io.StringIO()

        writer = csv.writer(output)

        writer.writerow(
            [
                "Visitor Name",
                "Phone",
                "Department ID",
                "Visit Date",
                "Status"
            ]
        )

        for visitor in visitors:

            writer.writerow(

                [

                    visitor.get(
                        "visitor_name",
                        ""
                    ),

                    visitor.get(
                        "visitor_phone",
                        ""
                    ),

                    visitor.get(
                        "department_id",
                        ""
                    ),

                    visitor.get(
                        "visit_date",
                        ""
                    ),

                    visitor.get(
                        "status",
                        ""
                    )

                ]

            )

        output.seek(0)

        return output.getvalue()

    def export_visitors_pdf(self):

        visitors = (
            self.visitor_repository
            .get_all_applications()
        )

        statistics = self.get_dashboard_statistics()

        buffer = io.BytesIO()

        document = SimpleDocTemplate(
            buffer
        )

        styles = getSampleStyleSheet()

        elements = []

        # ----------------------------

        elements.append(

            Paragraph(

                "<b><font size=22>"
                "Visitor Management System"
                "</font></b>",

                styles["Title"]

            )

        )

        elements.append(

            Paragraph(

                "<b>Visitor Analytics Report</b>",

                styles["Heading2"]

            )

        )

        elements.append(

            Paragraph(

                f"Generated On : "
                f"{datetime.now().strftime('%d %B %Y %I:%M %p')}",

                styles["Normal"]

            )

        )

        elements.append(

            Spacer(
                1,
                20
            )

        )

        # ----------------------------
        # Summary
        # ----------------------------

        summary = [

            ["Total Visitors", statistics["total_visitors"]],

            ["Today's Visitors", statistics["today_visitors"]],

            ["Approved", statistics["approved"]],

            ["Pending", statistics["pending"]],

            ["Rejected", statistics["rejected"]],

            ["Employees", statistics["total_employees"]],

            ["Departments", statistics["total_departments"]]

        ]

        summary_table = Table(summary)

        summary_table.setStyle(

            TableStyle(

                [

                    ("GRID",(0,0),(-1,-1),1,colors.black),

                    ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),

                    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

                    ("BOTTOMPADDING",(0,0),(-1,-1),8)

                ]

            )

        )

        elements.append(summary_table)

        elements.append(

            Spacer(
                1,
                25
            )

        )

        # ----------------------------
        # Visitor Table
        # ----------------------------

        table_data = [

            [

                "Visitor",

                "Phone",

                "Visit Date",

                "Status"

            ]

        ]

        for visitor in visitors:

            table_data.append(

                [

                    visitor.get(
                        "visitor_name",
                        ""
                    ),

                    visitor.get(
                        "visitor_phone",
                        ""
                    ),

                    visitor.get(
                        "visit_date",
                        ""
                    ),

                    visitor.get(
                        "status",
                        ""
                    )

                ]

            )

        table = Table(table_data)

        table.setStyle(

            TableStyle(

                [

                    ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

                    ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                    ("GRID",(0,0),(-1,-1),1,colors.black),

                    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

                    ("ALIGN",(0,0),(-1,-1),"CENTER"),

                    ("BOTTOMPADDING",(0,0),(-1,0),10)

                ]

            )

        )

        elements.append(table)

        document.build(elements)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf