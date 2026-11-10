Attribute VB_Name = "ExportSlidesPDF"
' ---------------------------------------------------------------------------
' Export every deck in the slides/ folder to PDF, using PowerPoint's own
' renderer. Run this after rebuilding the decks with tools/decks/deck_*.py.
'
' Why a macro: PowerPoint for Mac no longer honours the AppleScript
' "save ... as save as PDF" verb (it silently writes nothing), Keynote's
' .pptx import blocks on a modal dialog, and the decks use Calibri and
' Consolas, which live inside the Office bundle, so a third-party converter
' would substitute fonts.
'
' How to run it:
'   1. Open any deck from the slides/ folder in PowerPoint. The macro takes
'      the output folder from that presentation, so there are no paths to
'      edit, and opening it gives PowerPoint sandbox access to the folder.
'   2. Tools > Macro > Visual Basic Editor, then Insert > Module.
'   3. Paste this file's contents and press Run (F5) on ExportAllDecksToPDF.
'   4. A summary box reports how many of the decks exported.
' ---------------------------------------------------------------------------

Option Explicit

Private Const ppSaveAsPDF As Long = 32

Public Sub ExportAllDecksToPDF()
    Dim deckNames As Variant
    deckNames = Array( _
        "w1a_course_orientation", "w1b_intro_hyperspectral_eo", _
        "w1c_spectral_signatures_sensors", "w1d_data_access_exploration", _
        "w1e_preprocessing", "w2a_processing_workflows", _
        "w2b_feature_extraction", "w2c_material_discrimination_detection", _
        "w2d0_ml_primer_for_eo", "w2d_classification", "w2e_project_scoping", _
        "w3a_geoai_methods", "w3b_ai_assisted_mapping", "w3c_validation_accuracy", _
        "w3d_project_workshop_qa", "w4a_advanced_analytics", _
        "w4b_implementation_and_testing", "w4c_presentation_and_evaluation", _
        "wx_qgis_hypercoast")

    If ActivePresentation.Path = "" Then
        MsgBox "Open a deck from the slides folder first, then run this again.", vbExclamation
        Exit Sub
    End If

    Dim folder As String
    folder = ActivePresentation.Path & Application.PathSeparator

    Dim i As Long, exported As Long, problems As String
    For i = LBound(deckNames) To UBound(deckNames)
        Dim pptxPath As String, pdfPath As String
        pptxPath = folder & deckNames(i) & ".pptx"
        pdfPath = folder & deckNames(i) & ".pdf"

        Dim pres As Presentation
        Set pres = Nothing
        On Error Resume Next
        Set pres = Presentations.Open(pptxPath, ReadOnly:=msoTrue, WithWindow:=msoFalse)
        If Err.Number <> 0 Or pres Is Nothing Then
            problems = problems & vbCr & deckNames(i) & " - cannot open: " & Err.Description
            Err.Clear
        Else
            pres.SaveCopyAs pdfPath, ppSaveAsPDF
            If Err.Number <> 0 Then
                problems = problems & vbCr & deckNames(i) & " - cannot export: " & Err.Description
                Err.Clear
            Else
                exported = exported + 1
            End If
            pres.Close
            Err.Clear
        End If
        On Error GoTo 0
    Next i

    Dim total As Long
    total = UBound(deckNames) - LBound(deckNames) + 1
    If problems = "" Then
        MsgBox "Exported all " & total & " decks to PDF.", vbInformation
    Else
        MsgBox "Exported " & exported & " of " & total & " decks." & vbCr & problems, vbExclamation
    End If
End Sub
