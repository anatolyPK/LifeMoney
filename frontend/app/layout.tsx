import type {Metadata} from 'next'
import './globals.css'
import {NavLinks} from "@/app/ui/NavLinks";
import {AuthProvider} from "@/app/context/AuthContext";
import AuthButton from "@/app/components/AuthButton";
import UsernameProfile from "@/app/components/UsernameProfile";
import React from "react";

export const metadata: Metadata = {
    title: 'LifeMoney',
}


export default async function RootLayout({
                                       children,
                                   }: {
    children: React.ReactNode
}) {


    return (
        <html lang = "en">
          <body className= {"min-h-full bg-gray-100"}>
              <AuthProvider>
                   <header
                       className = {`px-4 py-5 bg-blue-400 shadow-xl text-xl text-white sticky top-0 flex flex-row justify-between items-center gap-6`}
                   >
                       <NavLinks />
                       <div className = {`flex flex-col gap-2 items-center`}>
                           <UsernameProfile />
                           <AuthButton />
                       </div>
                   </header>

                  <main>{children}</main>
              </AuthProvider>
          </body>
        </html>
    )
}