/**
 * Patient Detail — /patients/[patientId]
 * Live monitoring, infusion history, clinical notes
 */
export default function PatientDetailPage({
    params,
}: {
    params: { patientId: string };
}) {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">Patient Detail: {params.patientId}</h1>
            {/* TODO: Patient info + current IV card */}
            {/* TODO: Live telemetry (weight/flow charts) */}
            {/* TODO: Infusion history table */}
            {/* TODO: Clinical notes section */}
        </div>
    );
}
