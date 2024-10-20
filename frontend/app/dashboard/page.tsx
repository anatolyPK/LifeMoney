import ProtectedRoute from "@/app/components/ProtectedRoute";

export default  function Page() {

    return (
        <ProtectedRoute>
            <h1>Добро пожаловать на защищенную страницу!</h1>

        </ProtectedRoute>
    );
}
