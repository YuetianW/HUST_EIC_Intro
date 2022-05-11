/*
 * MtVerify.h
 *
 * Error handling for applications in
 * "Multitheading Applications in Win32"
 *
 * The function PrintError() is marked as __inline so that it can be
 * included from one or more C or C++ files without multiple definition
 * errors. For the examples in this book, this works fine.
 * To use the PrintError() in an application, it should be taken out,
 * placed in its own source file, and the "__inline" declaration removed
 * so the function will be globally available.
 */

#pragma comment( lib, "USER32" )

#include <crtdbg.h>
#define MTASSERT(a) _ASSERTE(a)


#define MTVERIFY(a) if (!(a)) PrintError(#a,__FILE__,__LINE__,GetLastError())

__inline void PrintError(LPSTR linedesc, LPSTR filename, int lineno, DWORD errnum)
{
	LPSTR lpBuffer;
	char errbuf[256];
#ifdef _WINDOWS
	char modulename[MAX_PATH];
#else // _WINDOWS
	DWORD numread;
#endif // _WINDOWS

	FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER
		| FORMAT_MESSAGE_FROM_SYSTEM,
		NULL,
		errnum,
		LANG_NEUTRAL,
		(LPTSTR)&lpBuffer,
		0,
		NULL);

	wsprintf(errbuf, "\nThe following call failed at line %d in %s:\n\n"
		"    %s\n\nReason: %s\n", lineno, filename, linedesc, lpBuffer);
#ifndef _WINDOWS
	WriteFile(GetStdHandle(STD_ERROR_HANDLE), errbuf, strlen(errbuf), &numread, FALSE);
	Sleep(3000);
#else
	GetModuleFileName(NULL, modulename, MAX_PATH);
	MessageBox(NULL, errbuf, modulename, MB_ICONWARNING | MB_OK | MB_TASKMODAL | MB_SETFOREGROUND);
#endif
	exit(EXIT_FAILURE);
}