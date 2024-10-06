
import LeftActionNavbar from "@/app/ui/LeftActionNavbar";
import RightActionNavbar from "@/app/ui/RightActionNavbar";
import ProtectedRoute from "@/app/components/ProtectedRoute";
import React from "react";


export default async function RootLayout({
                                             children,
                                         }: {
    children: React.ReactNode
}) {


    return (
        <ProtectedRoute>
            <div className={`flex flex-row mt-4 justify-center`}>
                <LeftActionNavbar />
                <div>{children}</div>
                <RightActionNavbar />
            </div>
        </ProtectedRoute>
    )
}